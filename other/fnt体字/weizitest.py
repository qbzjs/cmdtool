#!/usr/bin/python
#-*- coding: utf-8 -*-
import os
import chardet  #中文编码判断

qstr  = u"abc\u5023"
qstr  = u"abc\u0041"
qstr = u"abc\u6625"
qstr = qstr.encode('utf-8')
print qstr
# qstr  = u"abc\u0032"
qstr  = u"abc\u5023"
qstr = qstr.encode('utf-8')
print qstr

x = 0x6625
print x
x = 0x5023
print x

a = u'我'
tnu = repr(a)
print 'tnu:' + tnu
tin = str(tnu)
print 'tin:' + tin
print hex(ord(a))
print ord(a)

tmp = [u'零',u'一',u'二',u'三',u'四',u'五',u'六',u'七',u'八',u'九']
for x in tmp:
	print repr(x) + ':%s'%(x.encode('utf-8'))
# def conventStrTOUtf8(oldstr):
#     cnstrtype = chardet.detect(oldstr)['encoding']
#     utf8str =  oldstr.decode(cnstrtype).encode('utf-8')
#     return utf8str

# aaa = conventStrTOUtf8(qstr)
# print aaa
