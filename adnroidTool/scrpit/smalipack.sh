#!/bin/bash
export PATH=/Users/junpengzhang/Documents/android/apktool:$PATH
export PATH=/usr/bin/:$PATH
apktool b $1
cp -f hongbao.keystore ${1}/dist/hongbao.keystore
cp -f signedauto.exp ${1}/dist/signedauto.exp
cd ${1}/dist/
echo '开始签名，输入签名密码：123456'
expect signedauto.exp ${1}
echo '正在安装到手机'
adb install -r signed${1}.apk
echo '游戏重签名操作完成'