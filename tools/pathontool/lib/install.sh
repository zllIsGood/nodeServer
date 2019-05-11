#!/usr/bin/sh

cd `dirname $0` && SCRIPT_PATH=$(pwd)

svnPack='svn-0.3.45.tar.gz'
if [[ -e "$svnPack" ]];then
    tar xf $svnPack && cd svn-0.3.45
    python setup.py install
    cd .. && rm -rf svn-0.3.45
fi
