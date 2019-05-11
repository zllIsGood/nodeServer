update
差异化增量工具,使用python实现

功能描述:
1.取指定的svn间生成相应的差异量
2.生成更新描述文件
3.压缩相关文件
4.提交到svn目录,用于发布到cdn

环境要求:
cd lib && sudo sh ./install.sh

运行说明:
sh ./update.sh 100


客户端出包步骤:
1.客户端源码工程要先打包
sh ./publish.sh web
zhanhj/code/client/1.9.0 -> zhanhj/code/publish/1.9.0/web

2.发布到外网
cd zhanhj/code/publish/1.9.0/update/tool
sh ./update.sh 10901
a.先copy中转目录,提交到svn上
publish/1.9.0/web -> publish/1.9.0/update/web/res

b.计算差异化
publish/1.9.0/update/web/res
生成10901.json,10901.txt,10901.json.cfg

c.上传到ftp
index.html...

TODO:
1.ftp上传失败