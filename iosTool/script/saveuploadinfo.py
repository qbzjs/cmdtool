#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-11-10 11:28:17
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
import sys
import pinyin
def getStringName(hanyu):
	pname = pinyin.get_initial(hanyu,delimiter='').upper()
	return pname

if __name__=='__main__':
	args = sys.argv
	httppth = ''
	luobaoHttpth = ''
	appname = ''
	if len(args) > 3:
		appname = args[1]	#app中文名
		httppth = args[2]	#app绑定动态库后的ipa服务器地址
		luobaoHttpth = args[3]	#app祼包上传到服务器后的地址
	appEname = appname
	savestr = ''
	if httppth:
		savestr += appname + ',hook后ipa安装地址:\n-----\n' + httppth + '\n-----\n'
	if luobaoHttpth:
		savestr += appname + ',祼包下地址:\n-----\n' + luobaoHttpth + '\n-----\n'
	f = open('uploadname.txt','a')
	f.write(savestr)
	f.close()