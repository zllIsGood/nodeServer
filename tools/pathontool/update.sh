#!/bin/sh

if [ $# -ne 1 ] ;then
	echo "Usage:which ver" && exit
fi

ver=$1
shellPath=`pwd`
outPath=${shellPath}/../web/
sourcePath=${shellPath}/../../web
cdnPath=clientH5Union/res

function _commit(){
	path=$1
	echo "start commit $path ..."
	value=`svn st | grep "\?" | awk -F: '{print $1}'| cut -d' ' -f8`
	if [[ -n "$value" ]];then
		svn add $value
	fi

	# 删除旧文件
	value=`svn st | grep "\!" | awk -F: '{print $1}'| cut -d' ' -f8`
	if [[ -n "$value" ]];then
		svn del $value
	fi

	svn ci -m'M:自动打包提交'
}


resPath=${outPath}/res
verPath=${outPath}/ver
cfgPath=${outPath}/config.ini

# 先同步代码
cp -rf $sourcePath/ $resPath/
rm -rf $resPath/3rdlib
rm -rf $resPath/libs

# 提交到svn
targetPath=$resPath
pushd $targetPath
_commit $targetPath
popd

svn up ${resPath}
rev=`svn info ${resPath} | grep "Last Changed Rev" | awk -F: '{print $2}'| cut -d' ' -f2`

# 再计算差异
python diff.py $ver $rev $cfgPath

# 压缩json
pushd $verPath
zip $ver.json.cfg $ver.json
popd

# 提交差异到svn
targetPath=$verPath
pushd $targetPath
_commit $targetPath
popd

# 上传到cdn
rm -rf $outPath/tmp/$ver
mkdir -p $outPath/tmp/$ver
python ftpupload.py $ver $resPath $verPath $cdnPath $cfgPath
rm -rf $outPath/tmp

# 提交config.ini
targetPath=${outPath}
pushd $targetPath
_commit $targetPath
popd