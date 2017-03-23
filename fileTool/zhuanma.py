#!/usr/bin/env python
#-*- coding: utf-8 -*-
#可以通过此文件读取所有股票的ID和中文名，及所在版块信息
import os
import sys
import shutil
# import pinyin
import time
import copy
import chardet  #中文编码判断


reload(sys)
sys.setdefaultencoding( "utf-8" )


# print pinyin.get('你好')

# print pinyin.get('你好', format="strip", delimiter=" ")

# print pinyin.get('你好', format="numerical")
#中文转拼音
def getStringName(hanyu):
    #pname = pinyin.get_initial(hanyu,delimiter='').upper()
    pname = pinyin.get(hanyu, format="strip", delimiter="").lower()
    return pname
#提交数据到MySQL数据库


#获取文件名
def getFileNameFromPath(path):
    fname = os.path.splitext(os.path.split(path)[1])[0]
    return fname

def conventStrTOUtf8(oldstr):
    cnstrtype = chardet.detect(oldstr)['encoding']
    utf8str =  oldstr.decode(cnstrtype).encode('utf-8')
    return utf8str

def conventFileToUTF8(fpth):
    f = open(fpth,'r')
    dat = f.read()
    utf8dat = conventStrTOUtf8(dat)
    f.close()
    p,f = os.path.splitext(fpth)
    nfpth = p + '_utf8' + f
    f = open(nfpth ,'w')
    f.write(utf8dat)
    f.close()

#测试
if __name__ == '__main__':
    args = sys.argv
    fpth = ''
    if len(args) == 2 :
        if os.path.exists(args[1]):
            fpth = args[1]
        else:
            print "请加上要转码的文件路径"
    else:
        print "请加上要转码的文件路径"
    conventFileToUTF8(fpth)



# aaa = getStringName('中国')
# print aaa
        