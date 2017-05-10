#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-04-17 11:53:51
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os

count = 0
while True:
    print "count%d:"%(count)
    strin = raw_input()
    print 'input str is:%s'%(strin)
    print '选择操作, 输入数字编号 :'
    strin = raw_input()
    print 'input is:%s'%(strin)
    count += 1
    if strin == 'end' :
        break
