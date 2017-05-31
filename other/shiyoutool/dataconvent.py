#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-05-31 10:50:48
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
import sys
#获取脚本路径
def cur_file_dir():
    pathx = sys.argv[0]
    tmppath,_file = os.path.split(pathx)
    if cmp(tmppath,'') == 0:
        tmppath = sys.path[0]
    #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
    if os.path.isdir(tmppath):
        return tmppath
    elif os.path.isfile(tmppath):
        return os.path.dirname(tmppath)
    
#获取父目录
def GetParentPath(strPath):
    if not strPath:
        return None;
    lsPath = os.path.split(strPath);
    if lsPath[1]:
        return lsPath[0];
    lsPath = os.path.split(lsPath[0]);
    return lsPath[0];

#获取目录下的所有类型文件
def getAllExtFile(pth,fromatx = ".txt"):
    jsondir = pth
    jsonfilelist = []
    for root, _dirs, files in os.walk(jsondir):
        for filex in files:          
            #print filex
            name,text = os.path.splitext(filex)
            if cmp(text,fromatx) == 0:
                jsonArr = []
                rootdir = pth
                dirx = root[len(rootdir):]
                pathName = dirx +os.sep + filex
                jsonArr.append(pathName)
                (newPath,_name) = os.path.split(pathName)
                jsonArr.append(newPath)
                jsonArr.append(name)
                jsonfilelist.append(jsonArr)
            elif fromatx == ".*" :
                jsonArr = []
                rootdir = pth
                dirx = root[len(rootdir):]
                pathName = dirx +os.sep + filex
                jsonArr.append(pathName)
                (newPath,_name) = os.path.split(pathName)
                jsonArr.append(newPath)
                jsonArr.append(name)
                jsonfilelist.append(jsonArr)
    return jsonfilelist


def conventDataOneBlock(ldata):
    out = ''
    handdat = ldata[0].split()
    cmpdata = (int(handdat[1]) - 1)*5000 + int(handdat[2]) #注释：cmp=（线-1）*5000+点
    cmpstr = str(cmpdata)
    if len(cmpstr) < 8:
        ncmpstr = cmpstr
        for i in range(8-len(cmpstr)):
            ncmpstr = ' ' + ncmpstr
        cmpstr = ncmpstr

    newhand = 'SPNT   ' + cmpstr + '    ' + handdat[2] + '                          ' + handdat[1] + '\n'
    line1 = ''
    if len(handdat[3]) == 3:
        line1 = 'VELF   ' + cmpstr + '  ' + handdat[3]
    elif len(handdat[3]) == 4:
        line1 = 'VELF   ' + cmpstr + ' ' + handdat[3]
    elif len(handdat[3]) == 2:
        line1 = 'VELF   ' + cmpstr + '   ' + handdat[3]
    elif len(handdat[3]) == 1:
        line1 = 'VELF   ' + cmpstr + '    ' + handdat[3]
    else:
        line1 = 'VELF   ' + cmpstr + ' ' + handdat[3]
    out = out + newhand + line1
    isfirst = True
    for l in ldata[1:]:
        if isfirst:
            out = out + l
            isfirst = False
        else:
            out = out + 'VELF                ' + l 
    return out

def saveOutData(pth,dat):
    f = open(pth,'w')
    f.write(dat)
    f.close()

def conventData(fpth,saveName):
    f = open(fpth,'r')
    lines = f.readlines()
    f.close()
    datas = []
    tmpdata = []
    for l in lines:
        if l[0:7] == 'HEADVEL':
            if tmpdata:
                datas.append(tmpdata)
            tmpdata = []
            tmpdata.append(l)
        else:
            tmpdata.append(l)
    outstr = dian = '        CMP        点                            线\n'
    for d in datas:
        tmp = conventDataOneBlock(d)
        outstr = outstr + tmp
    outpth = 'out' + os.sep + saveName + '.txt'
    saveOutData(outpth, outstr)



def main():
    datfiles = getAllExtFile('data','.txt')
    fpths = {}
    for p in datfiles:
        tmpf = 'data' + p[0]
        fpths[p[2]] = tmpf
    for f in fpths.keys():
        conventData(fpths[f], f)
    print '所有数据转换完成'

#测试
if __name__ == '__main__':
    main()