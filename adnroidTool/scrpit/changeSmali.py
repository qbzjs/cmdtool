#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-11-14 10:52:10
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
import shutil
import sys
import hashlib



def isSameFile(f1pth,f2pth):
	f1 = open(f1pth,'r')
	a = f1.read()
	f1.close()
	f1hash = hashlib.sha256(a).hexdigest()
	f2 = open(f2pth,'r')
	b = f2.read()
	f2.close()
	f2hash = hashlib.sha256(b).hexdigest()
	if f1hash == f2hash:
		return True
	else:
		return False

uperchangestr = '''    invoke-static {}, Lcom/joyme/laiwanplugin/JMSDKPluginManager;->getInstance()Lcom/joyme/laiwanplugin/JMSDKPluginManager;

    move-result-object v0

    const/4 v1, 0x0

    invoke-virtual {v0,v1}, Lcom/joyme/laiwanplugin/JMSDKPluginManager;->OnRenderImage(I)V
'''

uperActiveOnCreate = '''    invoke-static {}, Lcom/joyme/laiwanplugin/JMSDKPluginManager;->getInstance()Lcom/joyme/laiwanplugin/JMSDKPluginManager;

    move-result-object v0

    invoke-virtual {v0, p0}, Lcom/joyme/laiwanplugin/JMSDKPluginManager;->init(Landroid/app/Activity;)V
'''

uperActiveOnDestroy = '''    invoke-static {}, Lcom/joyme/laiwanplugin/JMSDKPluginManager;->getInstance()Lcom/joyme/laiwanplugin/JMSDKPluginManager;

    move-result-object v0

    invoke-virtual {v0}, Lcom/joyme/laiwanplugin/JMSDKPluginManager;->onDestory()V
'''

uperActiveOnPause = '''    invoke-static {}, Lcom/joyme/laiwanplugin/JMSDKPluginManager;->getInstance()Lcom/joyme/laiwanplugin/JMSDKPluginManager;

    move-result-object v0

    invoke-virtual {v0}, Lcom/joyme/laiwanplugin/JMSDKPluginManager;->onPause()V
'''

uperActiveOnResume = '''    invoke-static {}, Lcom/joyme/laiwanplugin/JMSDKPluginManager;->getInstance()Lcom/joyme/laiwanplugin/JMSDKPluginManager;

    move-result-object v0

    invoke-virtual {v0}, Lcom/joyme/laiwanplugin/JMSDKPluginManager;->onResume()V
'''

def changeUnityPlayerFile(topth):
	f = open(topth,'r')
	oldstr = f.read()
	f.close()
	if oldstr.find('JMSDKPluginManager') != -1:
		print 'UnityPlayer已经嵌入过JMSDKPluginManager代码'
		return
	strlines = oldstr.split('\n')
	findline = 0
	for ln in range(len(strlines)):
		l = strlines[ln]
		if l.find('Lcom/unity3d/player/UnityPlayer;->nativeRender()Z') != -1:
			findline = ln
			break
	print findline
	if findline:
		print strlines[findline - 2]
		print strlines[findline - 1]
		print strlines[findline]
		strlines[findline - 2] = '    .locals 2'
		strlines[findline - 1] = '\n' + uperchangestr
		outstr = ''
		for nl in strlines:
			outstr += nl + '\n'
		f = open(topth,'w')
		f.write(outstr)
		f.close()
		print 'UnityPlayer嵌入smali的JMSDKPluginManager成功'
		return True
	else:
		print 'UnityPlayer中未找到nativeRender()Z方法嵌入JMSDKPluginManager失败'
		return False
#修改UnityPlayer
def changeUnityPlayerCalss(topth):
	print '查找并修改UnityPlayer.smali文件'
	uperpth = topth + '/UnityPlayer.smali'
	if not os.path.exists(uperpth):
		print 'UnityPlayer.smali文件不存在，可能apk有加密，或者apk包错误'
		return False
	libuperpth = 'lib/smali/com/unity3d/player/UnityPlayer.smali'
	libpth = 'lib/smali/com/unity3d/player/UnityPlayerChange.smali'
	if isSameFile(uperpth,libuperpth):
		print 'UnityPlayer与库中相同，使用替换文件方法嵌入JMSDKPluginManager代码'
		os.remove(uperpth)
		shutil.copyfile(libpth,uperpth)
	else:
		print '在smali中查找UnityPlayer;->nativeRender()Z方法并嵌入录屏代码'
		if changeUnityPlayerFile(uperpth):
			print 'UnityPlayer修改成功'
			return True
		else:
			print 'UnityPlayer修改失败'
			return False

def changeUnityPlayerActivityFile(topth):
	f = open(topth,'r')
	oldstr = f.read()
	f.close()
	if oldstr.find('JMSDKPluginManager') != -1:
		print 'UnityPlayerActivity已经嵌入过JMSDKPluginManager代码'
		return
	strlines = oldstr.split('\n')
	findonCreate = 0
	findonDestroy = 0
	findonPause = 0 
	findonResume = 0
	for ln in range(len(strlines)):
		l = strlines[ln]
		if l.find('Lcom/unity3d/player/UnityPlayer;->requestFocus()Z') != -1:
			findonCreate = ln
			continue
		if l.find('Lcom/unity3d/player/UnityPlayer;->quit()V') != -1:
			findonDestroy = ln
		if l.find('Landroid/app/Activity;->onPause()V') != -1:
			findonPause = ln
		if l.find('Landroid/app/Activity;->onResume()V') != -1:
			findonResume = ln
	print findonCreate,findonDestroy,findonPause,findonResume
	if findonCreate:
		print '修改onCreate方法，嵌入JMSDKPluginManager'
		print strlines[findonCreate]
		print strlines[findonCreate + 1]
		print strlines[findonCreate + 2]
		strlines[findonCreate + 1] = '\n' + uperActiveOnCreate
		print 'UnityPlayerActivity嵌入onCreate方法smali的JMSDKPluginManager成功'
	else:
		print 'UnityPlayerActivity中未找到onCreate方法,嵌入JMSDKPluginManager失败'
		return False
	if findonDestroy:
		print '修改onDestroy方法，嵌入JMSDKPluginManager'
		print strlines[findonDestroy]
		print strlines[findonDestroy + 1]
		print strlines[findonDestroy + 2]
		strlines[findonDestroy + 1] = '\n' + uperActiveOnDestroy
		print 'UnityPlayerActivity嵌入onDestroy方法smali的JMSDKPluginManager成功'
	else:
		print 'UnityPlayerActivity中未找到onDestroy方法,嵌入JMSDKPluginManager失败'
		return False
	if findonPause:
		print '修改onDestroy方法，嵌入JMSDKPluginManager'
		print strlines[findonPause]
		print strlines[findonPause + 1]
		print strlines[findonPause + 2]
		strlines[findonPause + 1] = '\n' + uperActiveOnPause
		print 'UnityPlayerActivity嵌入onPause方法smali的JMSDKPluginManager成功'
	else:
		print 'UnityPlayerActivity中未找到onPause方法,嵌入JMSDKPluginManager失败'
		return False
	if findonResume:
		print '修改onDestroy方法，嵌入JMSDKPluginManager'
		print strlines[findonResume]
		print strlines[findonResume + 1]
		print strlines[findonResume + 2]
		strlines[findonResume + 1] = '\n' + uperActiveOnResume
		print 'UnityPlayerActivity嵌入onResume方法smali的JMSDKPluginManager成功'
	else:
		print 'UnityPlayerActivity中未找到onResume方法,嵌入JMSDKPluginManager失败'
		return False
	outstr = ''
	for nl in strlines:
		outstr += nl + '\n'
	f = open(topth,'w')
	f.write(outstr)
	f.close()
	print 'UnityPlayerActivity所有JMSDKPluginManager相关方法嵌入成功'
	return True

#修改UnityPlayerActivity
def changeUnityPlayerActivityClass(topth):
	print '查找并修改UnityPlayerActivity.smali文件'
	upActivepth = topth + '/UnityPlayerActivity.smali'
	if not os.path.exists(upActivepth):
		print '游戏中UnityPlayerActivity.smali文件不存在'
		return False
	libupActivepth = 'lib/smali/com/unity3d/player/UnityPlayerActivity.smali'
	libpth = 'lib/smali/com/unity3d/player/UnityPlayerActivityChange.smali'
	if isSameFile(upActivepth,libupActivepth):
		print 'UnityPlayerActivity与库中文件相同，使用替换文件方法嵌入JMSDKPluginManager代码'
		os.remove(upActivepth)
		shutil.copyfile(libpth,upActivepth)
	else:
		print '在smali中查找UnityPlayerActivity的onCreate,onDestroy,onPause,onResume方法并嵌入录屏代码'
		if changeUnityPlayerFile(upActivepth):
			print 'UnityPlayerActivity修改成功'
			return True
		else:
			print 'UnityPlayerActivity修改失败'
			return False

def main(appname):
	oldjoymepth = 'lib/smali/com/joyme'
	joymepth = 'apks/'+ appname + '/smali/com/joyme'
	print oldjoymepth
	print joymepth
	if os.path.exists(joymepth):
		print 'apk有joyme目录，删除apk中的目录'
		shutil.rmtree(joymepth)
	print '复制joyme目录到游戏com目录中'
	shutil.copytree(oldjoymepth,joymepth)
	unityplayerpth = 'apks/'+ appname + '/smali/com/unity3d/player'
	changeUnityPlayerCalss(unityplayerpth)
	changeUnityPlayerActivityClass(unityplayerpth)


if __name__ == '__main__':
	args = sys.argv
	appname = ''
	if len(args) > 0:
		appname = args[1]
		main(appname)
	else:
		print 'createXML.py获取文件目录错误'