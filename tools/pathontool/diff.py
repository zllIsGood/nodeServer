#!/usr/bin/python
#-*- coding:utf-8 -*-
import os
import pprint
import svn.local
import svn.remote
import json
import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class LogHandler():
    # log_dict = dict()#上个版本的文件列表
    add_dict = dict()#增加文件列表
    del_dict = dict()#删除文件列表
    mod_dict = dict()#修改文件列表
    root_path = None #项目路径
    log_path = None #日志路径
    cur_version = None #版本号
    client = None #svn操作对象
    isRemote = False #是否远程操作
    def __init__(self):
        pass

    #获取客户端(本地or远程)
    def get_client(self,url_or_path):
        if url_or_path[0] == '/':
            self.isRemote = False
            return svn.local.LocalClient(url_or_path)
        else:
            self.isRemote = True
            return svn.remote.RemoteClient(url_or_path)
        pass
    pass

    #处理文件分类(增、删、改)
    def dealEntries(self,entries):
        for entry in entries:
            state = entry['item']
            path = entry['path']
            kind = entry['kind']
            if kind == 'file':
                path = path.replace(self.root_path+'/','')
                if state == 'added':
                    if self.del_dict.has_key(path):
                        del self.del_dict[path]

                    if not self.add_dict.has_key(path):
                        self.add_dict[path] = self.cur_version

                    print('   A {path}'.format(path = path))
                elif state == 'deleted':
                    if self.add_dict.has_key(path):
                        del self.add_dict[path]
                    
                    if self.mod_dict.has_key(path):
                        del self.mod_dict[path]

                    if not self.del_dict.has_key(path):
                        self.del_dict[path] = self.cur_version

                    print('   D {path}'.format(path = path))
                elif state == 'modified':
                    if self.add_dict.has_key(path):
                        del self.add_dict[path]

                    if not self.mod_dict.has_key(path):
                        self.mod_dict[path] = self.cur_version
                    
                    print('   M {path}'.format(path = path))
                else:
                    pass
            pass
        pass
    pass

    #获取某个区间段的提交记录
    def getRevisions(self,startRevision,endRevision):
        revisions = []
        try:
            entries = self.client.log_default(None,None,None,None,None,startRevision,endRevision)
            for entry in entries:
                revisions.append(entry.revision)
        except:
            print("revision error")
        
        return revisions
    pass

    # 获取某个提交记录的变动文件
    def getChangedEntries(self,revision):
        entries = []
        result = self.client.diff_summary(revision-1,revision)
        for entry in result:
            if not os.path.isdir(entry['path']):
                entries.append(entry)
        return entries
    pass

    # 获取某个区间段的所有变动文件
    def getAllChangedEntries(self,startRevision,endRevision):
        entriesArr = []
        revisions = self.getRevisions(startRevision,endRevision)
        for index in range(len(revisions)):
            revision = revisions[index]
            entries = self.getChangedEntries(revision)
            entriesArr.append(entries)
        return entriesArr
    pass

    # 输出日志路径
    def getLogPath(self,version,extensionName,outPath):
        log_dir = outPath
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        return '{logDir}/{version}.{extensionName}'.format(logDir=log_dir,version=version,extensionName=extensionName)
    pass

    # 变动日志dict转json
    def dict2Json(self,filePath,dictData):
        with open(filePath, 'w+') as json_file:
            json_file.write(json.dumps(dictData,sort_keys=True, indent=4, separators=(',', ':')))
        pass
    pass

    # 变动日志json转dict
    def json2Dict(self,filePath):
        json_dict = dict()
        with open(filePath) as json_file:
            data = json.load(json_file)
            for key,value in data.items():
                json_dict[key]= value
        return json_dict
        pass
    pass

    def dict2Txt(self,filePath,dictData,operator):
        with open(filePath, 'a') as json_file:
            for key in dictData:
                json_file.write("{operator} {key}\n".format(key=key,operator=operator))
            pass
    pass

    # 创建版本分支的第一份变动文件
    def executeFirst(self,root_path,version,revision,outPath):
        self.cur_version = version
        self.root_path = root_path
        self.client = self.get_client(self.root_path)
        # result = self.client.log_default(None,None,1)
        # for log in result:
        #     entries = self.getChangedEntries(log.revision)
        #     self.dealEntries(entries)
        entries = self.getChangedEntries(revision)
        self.dealEntries(entries)

        log_path = self.getLogPath(self.cur_version,"json",outPath)
        self.dict2Json(log_path,self.add_dict)
        config_dict['last_version'] = version
        config_dict['last_revision'] = revision
        self.dict2Json(config_path,config_dict)

        diff_path = self.getLogPath(self.cur_version,"txt",outPath)
        if os.path.exists(diff_path):
            os.remove(diff_path)
        self.dict2Txt(diff_path,self.add_dict,"A")
    pass

    # 版本分支补丁变动文件
    def excute(self,root_path,curVersion,startRevision,endRevision,outPath):
        self.root_path = root_path
        self.cur_version = curVersion
        self.client = self.get_client(self.root_path)
        entriesArr = self.getAllChangedEntries(startRevision,endRevision)
        for entries in entriesArr:
            self.dealEntries(entries)
        
        log_path = self.getLogPath(last_version,"json",outPath)
        log_dict = self.json2Dict(log_path)

        for key,value in self.add_dict.items():
            log_dict[key] = curVersion
        
        for key,value in self.mod_dict.items():
            log_dict[key] = curVersion

        log_path = self.getLogPath(curVersion,"json",outPath)
        self.dict2Json(log_path,log_dict)
        config_dict['last_version'] = curVersion
        config_dict['last_revision'] = endRevision
        self.dict2Json(config_path,config_dict)

        diff_path = self.getLogPath(curVersion,"txt",outPath)
        if os.path.exists(diff_path):
            os.remove(diff_path)
        self.dict2Txt(diff_path,self.add_dict,"A")
        self.dict2Txt(diff_path,self.del_dict,"D")
        self.dict2Txt(diff_path,self.mod_dict,"M")
    pass

svnLog = LogHandler()
curVersion = 0
if len(sys.argv) < 3:
    print("it needs 2 params at least.")
elif len(sys.argv) == 4:
    curVersion = int(sys.argv[1])
    revision = int(sys.argv[2])
    config_path = sys.argv[3]
    config_dict = svnLog.json2Dict(config_path)
    last_version = config_dict['last_version']
    last_revision = config_dict['last_revision']
    root_path = config_dict['root_path']
    out_path = config_dict['out_path']
    if last_revision == 0:
        print("start to excute...")        
        svnLog.executeFirst(root_path,curVersion,revision,out_path)
        print("execute finished.\n")    
    else:
        if revision != last_revision:
            if revision < last_revision:
                print("revision {revision} can't smaller than last revision {last_revision}".format(revision=revision,last_revision=last_revision))
            else:
                print("start to execute...")
                startRevision = last_revision + 1
                svnLog.excute(root_path,curVersion,startRevision,revision,out_path)
                print("execute finished.\n")
            pass
        else:
            print("revision {revision} has been executed!!!".format(revision=revision))
pass