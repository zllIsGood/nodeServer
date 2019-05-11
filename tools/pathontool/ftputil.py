# -*- coding: utf-8 -*-

import os
import sys
import time
import threading
from Queue import Queue
from ftplib import FTP as FTP_O

reload(sys)
sys.setdefaultencoding('utf-8')

# 重写ftp 修复同网段内 ip返回异常
class FTP(FTP_O):
	def connect(self, host='', port=0, timeout=-999):
		FTP_O.connect(self,host,port,timeout)
		self.host = host
		return self.welcome

	def makepasv(self):
		host,port = FTP_O.makepasv(self)
		return self.host,port

class FTPThread(threading.Thread):
	def __init__(self, ip, port, user, pwd, get_task ,callback):
		super(FTPThread, self).__init__()
		self._ftp = None
		self._finish_call = callback
		self._get_task = get_task
		self.ip = ip
		self.port = port
		self.user = user
		self.pwd = pwd
		
		# 一些老式的服务器不支持MLST 做个标记位处理
		self.use_MLST = True

	@property
	def ftp(self):
		if self._ftp == None:
			try:
				ftp = FTP()
				ftp.connect(self.ip,self.port)
				ftp.login(self.user,self.pwd)
				self._ftp = ftp
			except Exception, e:
				print(e)
				return None
		return self._ftp

	def __is_time_out_error(self,e):
		message = '%s'%e
		return 'ftplib.error_temp: 421' in message

	def __is_net_error(self,e):
		message = '%s'%e
		return 'Broken pipe' in message

	def __is_unknown_cmd(self,e):
		message = '%s'%e
		return '500 Unknown command' in message

	def __upload(self,ftp,task,finish_call):
		fi = None
		ex = None
		isSucc = True
		try:
			if task.isdir:
				self.mkdir(task.remote_path)
			else:
				cmd = 'STOR %s'%task.remote_path
				fi = open(task.local_path,'rb')
				ftp.storbinary(cmd,fi)
				fi.close()
		except Exception, e:
			isSucc = False
			try:
				if fi:fi.close()
			except Exception, ef:
				pass
			ex = e
			#print(self,ex,task.remote_path)
		finally:
			if ex == None:
				if finish_call:finish_call(self,task,isSucc)
			else:
				if self.__is_time_out_error(ex):
					raise IOError('ftplib.error_temp: 421')
				if self.__is_net_error(ex):
					raise IOError('32 Broken pipe')
				raise IOError('FTP error:%s'%ex)

	def upload_file(self,ftp,task,finish_call):
		# 文件类
		exist,r_size = self.is_exist(ftp,task.remote_path,task.isdir)
		
		# 检查是否已有该文件
		if exist:
			l_size = os.path.getsize(task.local_path)
			# 尺寸不对 删除 重传
			if l_size!=r_size:
				ftp.delete(task.remote_path)
				self.__upload(ftp,task,finish_call)
			else:
				# 尺寸相同 跳过
				if finish_call:finish_call(self,task,True)
		else:
			self.__upload(ftp,task,finish_call)

	def upload_folder(self,ftp,task,finish_call):
		exist,size = self.is_exist(ftp,task.remote_path,task.isdir)
		if exist:
			if finish_call:finish_call(ftp,task,True)
		else:self.__upload(ftp,task,finish_call)
	
	def is_exist(self,ftp,remote_path,isdir):
		size = None
		try:
			if isdir:
				if self.use_MLST:
					ftp.sendcmd('MLST %s'%remote_path)
				else:
					pwd = ftp.pwd()
					ftp.cwd(remote_path)
					ftp.cwd(pwd)
			else:
				ftp.voidcmd('TYPE I')
				size = ftp.size(remote_path)
			return True,size
		except Exception, e:
			# 不支持MLST 使用效率较差的方式
			if isdir and self.use_MLST and self.__is_unknown_cmd(e):
				self.use_MLST = False
				return self.is_exist(ftp,remote_path,isdir)
			else:
				return False,None

	def mkdir(self,path):
		self._ftp.mkd(path)

	def rmdir(self,r_path):
		def rmtree(ftp,path):
			f_list = ftp.nlst(path)
			ftp.sendcmd('TYPE I')
			for fi in f_list:
				fi_path = os.path.join(path,fi)
				try:
					ftp.size(fi_path)
					ftp.delete(fi_path)
				except Exception, e:
					rmtree(ftp,fi_path)
					ftp.rmd(fi_path)

		ftp = self._ftp
		rmtree(ftp,r_path)
		ftp.rmd(r_path)

	def run(self):
		ftp = self.ftp
		if ftp == None:return
		finish_call = self._finish_call
		task = self._get_task()
		while task!=None:
			try:
				# 文件夹
				if task.isdir:
					self.upload_folder(ftp,task,finish_call)
				else:
					self.upload_file(ftp,task,finish_call)
			except Exception, e:
				if finish_call:finish_call(ftp,task,False)
				# 超时
				if self.__is_time_out_error(e) or self.__is_net_error(e):
					ftp = None
					#self._ftp = None
					print('')
					print(self,'break',e)
					break
				#else:
					#print('')
					#print("ftp error:",task.remote_path,e)
			finally:
				if ftp:task = self._get_task()
		self.close()
		pass

	def close(self):
		try:
			if self._ftp:
				self._ftp.quit()
		except Exception, e:
			pass
		pass

class FileInfo(object):
	def __init__(self, local_path,remote_path,isdir=False):
		super(FileInfo, self).__init__()
		self.isdir = isdir
		self.local_path = local_path
		self.remote_path = remote_path
		
class FTPUploadTask(object):
	def __init__(self):
		super(FTPUploadTask, self).__init__()
		self.task_lock = threading.Lock()
		self.count_lock = threading.Lock()
		
		self.task_queue = Queue()
		self._thread_queue = Queue()
		self.task_faild_queue = Queue()

		self._succ_count = 0
		self._faild_count = 0
		self._total_count = 0
		self._retry_count = 0
		self._max_retry_count = 3

		self._thread_count = 4
		self.upload_file_info = None
		
	def __gen_task(self,local_path,remote_path,task_queue):
		# 屏蔽所有隐藏文件
		if os.path.basename(local_path)[0] == '.':
			return
		isdir = os.path.isdir(local_path)
		file_info = FileInfo(local_path,remote_path,isdir)
		task_queue.put(file_info)
		if isdir:
			for fi_name in os.listdir(local_path):
				fi_path = os.path.join(local_path,fi_name)
				re_path = os.path.join(remote_path,fi_name)
				self.__gen_task(fi_path,re_path,task_queue)
		pass

	def __get_task(self):
		if self.task_lock.acquire():
			task = None
			if not self.task_queue.empty():
				task = self.task_queue.get()
			##print('get task',task)
			self.task_lock.release()
			return task
		pass

	def __start_upload(self,file_info,thread_count):
		if self.task_queue.empty() or file_info==None:return

		# 先处理remote_path
		if self.__create_remote_folder(file_info) == False:
			return
		self.logtime('start:')
		self._succ_count = 0
		self._faild_count = 0
		self._total_count = self.task_queue.qsize()

		task_thread = None
		thread_count = thread_count>self.task_queue.qsize() and self.task_queue.qsize() or thread_count
		self._thread_count = thread_count

		for i in range(thread_count):
			task_thread = FTPThread(self.ip,self.port,self.user,self.pwd,self.__get_task,self.__finish_upload)
			self._thread_queue.put(task_thread)
			task_thread.start()

		while not self._thread_queue.empty():
			task_thread = self._thread_queue.get()
			task_thread.join()
			pass

		self.__finish_all_task()
		pass

	def __finish_upload(self,FTPObject,task,isSucc):
		if self.count_lock.acquire():
			if isSucc:
				self._succ_count = self._succ_count+1
			else:
				self._faild_count = self._faild_count+1
				self.task_faild_queue.put(task)
			self.count_lock.release()
			self.update_progress()

	def __finish_all_task(self):
		print('') # 清掉进度条的\r
		self.logtime('finish:')
		if self.task_faild_queue.empty():
			print('【 cdn all done！】')
		else:
			self.__retry()

	def __create_remote_folder(self,file_info):
		remote_path = file_info.remote_path
		# 非文件夹或根目录 直接返回
		if not file_info.isdir or remote_path == '' or remote_path == '/':
			return True

		# ftp创建
		ftp_thread = FTPThread(self.ip,self.port,self.user,self.pwd,self.__get_task,self.__finish_upload)
		ftp = ftp_thread.ftp
		if ftp == None:
			return False

		# 检测远程文件夹是否创建
		isexist,size = ftp_thread.is_exist(ftp,remote_path,True)
		if isexist:return True
		
		# 检测哪一层文件夹没创建
		test_folder = remote_path
		path_list = []
		while test_folder!='':
			isexist,size = ftp_thread.is_exist(ftp,test_folder,True)
			if isexist:
				test_folder = ''
			else:
				path_list.append(test_folder)
				test_folder = os.path.dirname(test_folder)
			pass

		if len(path_list)==0:
			return True

		# 文件夹逐层创建
		try:
			while len(path_list)>0:
				ftp_thread.mkdir(path_list.pop())
				pass
			ftp_thread.close()
		except Exception, e:
			print('create folder',e)
			ftp_thread.close()
			return False
		return True

	def __retry(self):
		if self._retry_count<self._max_retry_count:
			self._retry_count = self._retry_count+1
			while not self.task_faild_queue.empty():
				self.task_queue.put(self.task_faild_queue.get())
				pass

			print('[retry] faild:%s retry:%s max:%s'%(self.task_queue.qsize(),self._retry_count,self._max_retry_count))
			sys.stdout.flush()
			# 重启上传
			self.__start_upload(self.upload_file_info,self._thread_count)
		else:
			self.__echo_faild_list()

	def __echo_faild_list(self):
		print('\n------faild list-------')
		sys.stdout.flush()
		while not self.task_faild_queue.empty():
			file_info = self.task_faild_queue.get()
			print('faild upload: %s'%file_info.remote_path)
			sys.stdout.flush()
		print('------faild list end-------')

	def set_connect(self,ip,port,user,pwd):
		self.ip = ip
		self.port = port
		self.user = user
		self.pwd = pwd

	def upload(self,local_path,remote_path,thread_count=4):
		self.upload_file_info = FileInfo(local_path,remote_path,os.path.isdir(local_path))
		self.__gen_task(local_path,remote_path,self.task_queue)
		self._total_count = self.task_queue.qsize()
		self.__start_upload(self.upload_file_info,thread_count)
		pass

	def add_task(self,file_info):
		self.task_queue.put(file_info)
		self._total_count = self._total_count+1

	def update_progress(self):
		thread = self._total_count-self.task_queue.qsize()-self._succ_count-self.task_faild_queue.qsize()
		thread = thread != 0 and thread+1 or 0
		print('\rtotal:%s succ:%s faild:%s thread:%s'%(self._total_count,self._succ_count,self.task_faild_queue.qsize(),thread)),
		sys.stdout.flush()
		pass

	def logtime(self,desc):
		sys.stdout.flush()
		tim = time.localtime(time.time())
		print('%s %sh %sm %ss'%(desc,tim.tm_hour,tim.tm_min,tim.tm_sec))
		sys.stdout.flush()
		pass