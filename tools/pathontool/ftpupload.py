# -*- coding: utf-8 -*-

# 上传资源到cdn

import os
import sys
import json
import shutil
from ftputil import FTPUploadTask, FTPThread

reload(sys)
sys.setdefaultencoding('utf-8')

def read(filePath):
    json_dict = dict()
    with open(filePath) as json_file:
        data = json.load(json_file)
        for key, value in data.items():
            json_dict[key]= value
    return json_dict

def upload(version, local_path, remote_path, files, config_path):
    cfgs = read(config_path)
    cdn_cfg = cfgs['cdn_info']

    ftp = FTPUploadTask()
    ftp.set_connect(cdn_cfg['host'], cdn_cfg['port'], cdn_cfg['user'], cdn_cfg['pwd'])
    task_thread = FTPThread(ftp.ip, ftp.port, ftp.user, ftp.pwd, None, None)

    if version > 0:
        is_exist, size = task_thread.is_exist(task_thread.ftp, remote_path, True)

        if is_exist:
            print('version [%s] is exists, remote [%s]' % (version, remote_path))
            return True

    # 上传
    if files is None:
        print('upload path [%s]...' % local_path)
        ftp.upload(local_path, remote_path, 8)
    else:
        # 只能上传已存在的目录
        for f in files:
            fpath = os.path.join(local_path, f)
            print('upload file [%s]...' % fpath)
            ftp.upload(fpath, os.path.join(remote_path, f), 1)

    print('upload finish')

    pass

def readDiff(fname):
    # 从ver.txt内读取出差异表(A M开头及resource开头的)
    content = []
    with open(fname, 'r') as f:
        for line in f.readlines():  
            line = line.strip('\n')
            if line.find("M ") == 0:
                line = line.replace("M ", "")
            elif line.find("A ") == 0:
                line = line.replace("A ", "")

            content.append(line)

    return content

if __name__ == '__main__':
    ver = sys.argv[1]
    res_path = sys.argv[2]
    ver_path = sys.argv[3]
    remote_path = sys.argv[4]
    cfg_path = sys.argv[5]

    lines = readDiff(os.path.join(ver_path, ver) + '.txt')
    index_files = []
    upload_files = []
    main_files = []

    for line in lines:
        if line.find("resource") == 0:
            upload_files.append(line)
        elif line.find("main.min.js") == 0:
            main_files.append(line)
        else:
            index_files.append(line)

    # 生成一份cdn目录结构
    tmp_path = os.path.join(res_path, '../tmp', ver)
    if len(upload_files) > 0:
        for f in upload_files:
            path = os.path.dirname(os.path.join(tmp_path, f))
            if not os.path.exists(path):
                os.makedirs(path)
            shutil.copyfile(os.path.join(res_path, f), os.path.join(tmp_path, f))

    ver_files = []
    ver_files.append(ver + '.json')
    ver_files.append(ver + '.json.cfg')
    for f in ver_files:
        path = os.path.dirname(os.path.join(tmp_path, f))
        if not os.path.exists(path):
            os.makedirs(path)
        shutil.copyfile(os.path.join(ver_path, f), os.path.join(tmp_path, f))
    
    # 上传    
    upload(ver, os.path.join(res_path, '../tmp', ver), os.path.join(remote_path, ver), None, cfg_path)
    
    # 上传index.html
    if len(index_files) > 0:
        upload(-1, res_path, remote_path, index_files, cfg_path)

    # 上传main.min.js,main.min.js.cfg
    if len(main_files) > 0:
        upload(-1, res_path, remote_path + "/" + ver, main_files, cfg_path)

    pass
