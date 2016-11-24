#!bin/bash
#create buy zhangjunpeng @ 2016
export PATH=/usr/local/bin/:$PATH
pwdpth=`pwd`
cocos2dDir="cocos2dx"
Unity3DDir='u3d'
otherDir='other'
# find $2|grep "/.$1/>"
C2DIpas=`find $cocos2dDir -name '*.ipa' -type f`
U3DIpas=`find $Unity3DDir -name '*.ipa' -type f`
OtherIpas=`find $otherDir -name '*.ipa' -type f`
echo $C2DIpas

hookfile=`find lib -name 'hook.dylib' -type f`
SDKbundle=`find lib -name 'JoymeVideoSDK.bundle'`
echo '发现hook文件'
echo $hookfile
echo $SDKbundle

if [[ $C2DIpas ]]; then
	echo '有cocos2d-x的ipa包,开始处理cocos2d-x游戏包...'
fi

countfile()
{
	c2darr=($1)
	num=${#c2darr[@]} 
	echo $num
}

if [[ ! -f $hookfile ]]; then
	echo '没有在脚本目录找到hook.dylib文件'
	exit
fi
if [[ ! -d $SDKbundle ]]; then
	echo '没有在脚本目录找到JoymeVideoSDK.bundle资源文件'
	exit
fi

#解压ipa包
UnZIPIpa()
{
	fname=$1
	echo '解包ipa:'${fname}
	unzip -q $1 
}

#获取路径中的文件名
getFName()
{
	var="$1"
	tmp=${var##*/}
	echo ${tmp%.*}
}

bindRunFileAndHook()
{
	
	exef=$1
	hookf=$2
	echo '绑定可执行文件和hook文接接口....'${exef}${hookf}
	yololibpth=${pwdpth}'/lib/yololib'
	$yololibpth  "$exef" "$hookf"
}

#app签名
codesignApp()
{
	appnametmp=$1
	echo '使用证书签名app:'${appnametmp}
	codesign -f -v -s "iPhone Distribution: Enjoy Found (Beijing)Technology Development Co.,Ltd." --entitlements $entitlementsPlistFile "$appdir"
}

codesinFIle()
{
	echo '使用证书签名文件'${1}
	codesign -f -v -s "iPhone Distribution: Enjoy Found (Beijing)Technology Development Co.,Ltd." "$1"
}

#ios10之后要求Info.plist要加入麦克风,照像机和照片库权限
xmlEditAddKey()
{
	xmlpth=${1}
	python script/xmlEdit.py ${xmlpth}
}


#替找证书文件
ReplaceProv()
{
	#找出app子文件夹名
	appdir=`find Payload -name "*.app" -type d`
	if [[ ! $appdir ]]; then
		echo '没有解压成功,Payload没有找到解压后的app包'
		exit
	fi
	echo '找到app目录:'
	echo $appdir
	echo '修改Info.plist文件，加入三个录屏相关权限'
	echo '先将plist二进制文件转为xml1文件'
	infoplist=${appdir}/Info.plist
	echo 'Info.plist--->'${infoplist}
	plutil -convert xml1 ${infoplist}
	cp -f ${infoplist} Info.plist
	`xmlEditAddKey ${infoplist}`
	echo '请把企业证书和相关plist文件放在脚本同一目录下'
	mobileprovisionFile=`find . -maxdepth 1 -name '*.mobileprovision'`
	if [[ ! $mobileprovisionFile ]]; then
		echo '错误:未发现mobileprovision格式证书文件'
		echo '请参考:http://www.lhjzzu.com/2016/05/03/ios-ipa-codesign/#section-7'
		exit
	fi
	entitlementsPlistFile=`find . -maxdepth 1  -name 'entitlements.plist'`
	if [[ ! $entitlementsPlistFile ]]; then
		echo '错误:未发现entitlements.plist文件'
		exit '请参考:http://www.lhjzzu.com/2016/05/03/ios-ipa-codesign/#section-7'
	fi
	appdirembe=${appdir}'/embedded.mobileprovision'
	echo '复制embedded.mobileprovision到app目录'
	echo $appdirembe
	echo $mobileprovisionFile
	cp -f $mobileprovisionFile "$appdirembe"
	echo '复制hook动态库文件到app中'
	hooktmp=${appdir}'/hook.dylib'
	echo $hooktmp
	echo $hookfile
	cp -f $hookfile "$hooktmp"
	echo '复制JoymeVideoSDK.bundle资源文件到app中'
	echo $SDKbundle
	bundleapp=${appdir}'/JoymeVideoSDK.bundle'
	echo $bundleapp
	if [[ "$bundleapp" ]]; then
		rm -r "$bundleapp"
	fi
	cp -r -f $SDKbundle "$bundleapp"
	exefileName=`getFName "$appdir"`
	echo $exefileName
	exifilepth=${appdir}'/'${exefileName} 
	#绑定可执行文件和动态库文件
	echo $exifilepth
	echo $hooktmp
	cd "$appdir"
	bindRunFileAndHook "$exefileName" "hook.dylib"
	cd "$pwdpth"
	echo '签名hook.dylib动态库文件'
	hookappfile=${appdir}'/hook.dylib'
	codesinFIle "$hookappfile"
}

zipApp()
{	fname=$1
	fpthtmp=`dirname "$fname"`
	fnametmp=`basename "$fname"`
	nfname=${fpthtmp}'/hooked_'${fnametmp%%-*}
	zip -q -r  "$nfname" Payload
	echo $nfname
}


removePayload()
{
	if [[  -d Payload  ]]; then
		echo '删除Payload目录...'
		rm -r Payload
	fi
}

if [[  -d out  ]]; then
	echo '输出目录out存在,删除out目录...'
	rm -r out
fi
echo '创建输出目录:out'
mkdir out
mkdir out/cocos2dx
mkdir out/u3d
mkdir out/other
echo '删除Payload目录'
removePayload

echo $C2DIpas

deviceids=`idevice_id -l`

for tmp in $C2DIpas
do
	echo '解压文件:'${tmp}
	UnZIPIpa $tmp	
	echo '替换证书...'
	ReplaceProv		
	codesignApp
	echo '重新打包ipa包,输出到out相应目录'
	outdir='out/'${tmp}
	echo $outdir
	#打包ipa后返回包路径，方便马上安装
	endipa=`zipApp "$outdir"`
	removePayload
	echo ${tmp}'文件签名完成'
	echo '安装ipa到手机:'${endipa}
	if [[ $deviceids ]]; then
		echo '有手机连接，将把ipa包自动安装到手机'
		ideviceinstaller -i "$endipa"
	fi
done

if [[ $deviceids ]]; then
	echo '有手机连接，如果正常ipa包将自动安装到手机'
fi

echo '所有cocos2d-x目录ipa文件签名完成，请在out目录cocos2d-x中查找....'
for tmp in $U3DIpas
do
	echo '解压文件:'${tmp}
	UnZIPIpa $tmp	
	echo '替换证书...'
	ReplaceProv		
	codesignApp
	echo '重新打包ipa包,输出到out相应目录'
	outdir='out/'${tmp}
	echo $outdir
	#打包ipa后返回包路径，方便马上安装
	endipa=`zipApp "$outdir"`
	removePayload
	echo ${tmp}'文件签名完成'
	echo '安装ipa到手机:'${endipa}
	if [[ $deviceids ]]; then
		echo '有手机连接，将把ipa包自动安装到手机'
		ideviceinstaller -i "$endipa"
	fi
done

if [[ $deviceids ]]; then
	echo '有手机连接，如果正常ipa包将自动安装到手机'
fi
echo '所有u3d目录ipa文件签名完成，请在out目录u3d中查找....'

for tmp in $OtherIpas
do
	echo '解压文件:'${tmp}
	UnZIPIpa $tmp	
	echo '替换证书...'
	ReplaceProv		
	codesignApp
	echo '重新打包ipa包,输出到out相应目录'
	outdir='out/'${tmp}
	echo $outdir
	#打包ipa后返回包路径，方便马上安装
	endipa=`zipApp "$outdir"`
	removePayload
	echo ${tmp}'文件签名完成'
	echo '安装ipa到手机:'${endipa}
	if [[ $deviceids ]]; then
		echo '有手机连接，将把ipa包自动安装到手机'
		ideviceinstaller -i "$endipa"
	fi
done

echo '所有other目录ipa文件签名完成，请在out目录other中查找....'
if [[ $deviceids ]]; then
	echo '有手机连接，如果正常ipa包将自动安装到手机'
fi
