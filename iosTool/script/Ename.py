#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-11-10 11:28:17
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$
import sys
import pinyin

def getStringName(hanyu):
	pname = pinyin.get_initial(hanyu,delimiter='').upper()
	return pname
if __name__=='__main__':
	args = sys.argv
	appname = ''
	if len(args) > 0:
		appname = args[1]
	appEname = getStringName(appname)
	print appEname