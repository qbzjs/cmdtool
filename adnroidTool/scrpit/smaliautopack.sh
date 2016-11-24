#!/bin/bash
export PATH=/Users/junpengzhang/Documents/android/apktool:$PATH
export PATH=/usr/bin/:$PATH

if [[ ! -d apks ]]; then
    mkdir apks
fi

if [[ ! -d backxml ]]; then
    mkdir backxml
fi

if [[ ! -f "apks/smalipack.sh" ]]; then
    cp -f lib/scrpit/smalipack.sh apks/smalipack.sh
fi
if [[ ! -f "apks/signedauto.exp" ]]; then
    cp -f lib/scrpit/signedauto.exp apks/signedauto.exp
fi
if [[ ! -f "apks/hongbao.keystore" ]]; then
    cp -f lib/scrpit/hongbao.keystore apks/hongbao.keystore
fi

uapkPTH='unpackAPK'

unpackapks=`find $uapkPTH -name '*.apk' -type f`

repackAPK()
{
    echo '开始集成录屏sdk到游戏apks/'${1}'.apk'
    echo '复制要集成的apk包到apks目录'
    APKPTH='unpackAPK/'${1}'.apk'
    APKPTHWORK='apks/'${1}'.apk'
    cp -f ${APKPTH} ${APKPTHWORK}
    echo '解包游戏apk包'
    cd apks
    apktool d ${1}'.apk'
    gameUnityso=${1}'/lib/armeabi-v7a/libunity.so'
    if [ ! -f ${gameUnityso} ]; then 
        echo ${1}'不是一个unity引擎开发的游戏'
        return
    fi 
    cd ..
    echo '复制Laiwan.apk到游戏资源目录'
    cp -f lib/assets/ShareSDK.xml apks/${1}/assets/ShareSDK.xml
    cp -f lib/assets/Laiwan.apk apks/${1}/assets/Laiwan.apk
    echo '修改游戏原来AndroidManifest.xml文件，加入sdk相应权限以及sdk包的appID'
    python createXML.py ${1}
    echo '增加sdk相关smali程序到游戏smali中'
    python changeSmali.py ${1}
    echo '重新打开修改后的apk游戏'
    cd apks
    sh smalipack.sh ${1}
    cd ..
    #rm 'apks/'${1}'/dist/'${1}'.apk'
    echo '游戏打包完成,在下边目录找到集成录屏后并重新临时签名的apk安装包:'
    echo 'apks/'${1}'/dist/signed'${1}'.apk'
    
}

#获取路径中的文件名
getFName()
{
    var="$1"
    tmp=${var##*/}
    echo ${tmp%.*}
}

echo $unpackapks
#解包所有apk并集成录屏sdk
for tmp in $unpackapks
do
    echo $tmp
    apkname=`getFName ${tmp}`
    repackAPK ${apkname}
done
echo '所有apk都已集成结束'