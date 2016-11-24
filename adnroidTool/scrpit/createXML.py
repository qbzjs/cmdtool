#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-11-14 10:52:10
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
import sys
#ini解析库
import ConfigParser
#xml解析库
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

import changeSmali

def parse_and_get_ns(file):
    events = "start", "start-ns"
    root = None
    ns = {}
    for event, elem in ET.iterparse(file, events):
        if event == "start-ns":
            if elem[0] in ns and ns[elem[0]] != elem[1]:
                # NOTE: It is perfectly valid to have the same prefix refer
                #     to different URI namespaces in different parts of the
                #     document. This exception serves as a reminder that this
                #     solution is not robust.    Use at your own peril.
                raise KeyError("Duplicate prefix with different URI found.")
            ns[elem[0]] = "{%s}" % elem[1]
        elif event == "start":
            if root is None:
                root = elem
    return ET.ElementTree(root), ns


#获取sdk要求设置的权限(读取lib/xml/uses-permission.permi文件中要设置的权限)
def getPerSetPermission():
	tree = ET.ElementTree(file='lib/xml/uses-permission.permi')
	root = tree.getroot()
	chs = root.getchildren()
	permissiontmp = []
	for c in chs:
		permissiontmp.append(c.attrib.values()[0])
	return permissiontmp

#获取sdk为当前游戏设置的SDK appID和key
def getPerSetKey():
	f = open('lib/xml/meta-data.keydata','r')
	dat = f.read()
	f.close()
	dat = dat.replace('\t','')
	dat = dat.replace(' ','')
	print '当前设置的录屏SDK相关key'
	print dat
	datdic = {}
	datls = dat.split('\n')
	for d in datls:
		if d.find('=') != -1:
			ds = d.split('=')
			datdic[ds[0]] = ds[1]
	return datdic

def getPerActive():
	tree = ET.ElementTree(file='lib/xml/weixin.activity')
	root = tree.getroot()
	return root.getchildren()[0]

def wrteXMLToFilePath(tree,pth):
	print '保存最终生成AndroidManifest.xml'
	print pth
	tree.write(pth, encoding="utf-8",xml_declaration=True) 

def createPermissionNode(xmlns,mission):
	property_map = {xmlns['android'] + 'name':mission}
	element = ET.Element('uses-permission', property_map)  
	return element

def createMetaDataNode(xmlns,metadic):
	eles = []
	for k in metadic.keys():
		property_map = {xmlns['android'] + 'name':k,xmlns['android']+'value':metadic[k]}
		element = ET.Element('meta-data', property_map)  
		eles.append(element)
	return eles

#查找原xml文件中是原有微信分享active
def testWeixinActive(xmlpth):
	#wxapi.WXEntryActivity
	f = open(xmlpth,'r')
	s = f.read()
	f.close()
	pthtmp,xname = os.path.split(xmlpth)
	_tmp,appname = os.path.split(pthtmp)
	print '备份AndroidManifest.xml文件到backxml/' + appname + '目录'
	nxmlpth = 'backxml/'+ appname + '/' + xname 
	if not os.path.exists('backxml/'+ appname):
		os.mkdir('backxml/'+ appname)
	fnew = open(nxmlpth,'w')
	fnew.write(s)
	fnew.close()
	if s.find('wxapi.WXEntryActivity') != -1:
		return True
	else:
		return False
def decodeAndroidManifest(xmlpth):
	ET.register_namespace('android', 'http://schemas.android.com/apk/res/android')
	tree,xmlns = parse_and_get_ns(xmlpth)
	print xmlns
	root = tree.getroot()
	chs = root.getchildren()
	permissions = []
	print len(chs)
	for c in chs:
		if c.tag == 'uses-permission':
			permissions.append(c.attrib.values()[0])
	permis = getPerSetPermission()
	nomis = []
	for p in permis:
		if p not in permissions:
			nomis.append(p)
	if not nomis:
		print '游戏原有AndroidManifest中已包含所有需要权限'
	else:
		print '下边所需要权限将加入游戏AndroidManifest.xml文件中:'
		for cmis in nomis:
			print cmis
			addmis = createPermissionNode(xmlns,cmis)
			root.append(addmis)
	sdkkeydic = getPerSetKey()		#sdk设置的appid和sdkkey
	app = root.find('application')
	appchs = app.getchildren()
	appActives = []
	for d in appchs:
		if d.tag == 'activity':
			appActives.append(d)
		elif d.tag == 'meta-data':
			if d.attrib.values()[1] in sdkkeydic.keys():
				d.attrib.values()[0] = sdkkeydic[d.attrib.values()[1]]
				sdkkeydic.pop(d.attrib.values()[1])
	if sdkkeydic:
		print '为application设置录屏appID'
		dics = createMetaDataNode(xmlns,sdkkeydic)
		for met in dics:
			root.find('application').append(met)
	else:
		print 'application已经有录屏sdk相关appkey'
	isHeaveWeiXin = False
	if not testWeixinActive(xmlpth):#查看原xml文件是否已有微信分享,如果没有，则加上
		print '游戏没有微信界面，为游戏添加微信Active'
		weixinActive = getPerActive()
		root.find('application').append(weixinActive)
	else:
		print '游戏中已有微信分享界面'
	wrteXMLToFilePath(tree,xmlpth)

def main(appfilename):
	apkxmlpth = 'apks/'+ appfilename +'/AndroidManifest.xml'
	decodeAndroidManifest(apkxmlpth)
	print 'xml文件设置转换完成\n'
	print '开始修改java对象文件'

if __name__ == '__main__':
	args = sys.argv
	appname = ''
	if len(args) > 0:
		appname = args[1]
		main(appname)
	else:
		print 'createXML.py获取文件目录错误'