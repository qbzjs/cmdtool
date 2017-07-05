#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

#批量wav转为map3格式
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
def getAllExtFile(pth,fromatx = ".erl"):
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


#获取一个目录下的所有子目录路径
def getAllDirs(spth):
    files = getAllExtFile(spth,'.*')
    makedirstmp = []
    isOK = True
    # 分析所有要创建的目录
    for d in files:
        if d[1] != '/' and (not d[1] in makedirstmp): #创建未创建的目录层级
            tmpdir = d[1][1:]
            tmpleves = tmpdir.split('/')
            alldirs = getAllLevelDirs(tmpleves)
            for dtmp in alldirs:
                if not dtmp in makedirstmp:
                    makedirstmp.append(dtmp)
    return makedirstmp
#获取目录下的所有文件路径
def getAllFiles(spth):
    files = getAllExtFile(spth,'.*')
    makedirstmp = []
    isOK = True
    # 分析所有要创建的目录
    for d in files:
        makedirstmp.append(d[0])
    return makedirstmp


def isFile(filename):
    try:
        with open(filename) as f:
            return True
    except IOError:
        return False

def finddir(arg,dirname,filenames):
    name,text = os.path.split(dirname)
    dirnametmp = str(dirname)
    if text and text[0] == '.':
        print dirname
        print filenames
        os.system('rm -r %s'%(dirname))
        return
    elif filenames:
        for f in filenames:
            if f[0] == '.' and isFile(dirname + f):
                fpthtmp = dirname + f
                if f.find(' '):
                    nf = f.replace(' ','\ ')
                    fpthtmp = dirname + nf
                print dirname + f
                os.system('rm  %s'%(fpthtmp))

#删除所有pth目录下的所有"."开头的文件名和目录名
def removeProjectAllHideDir(pth):
    alldirs = getAllDirs(pth)
    if not ('/' in alldirs):
        alldirs.append('/')
    for d in alldirs:
        tmpth = pth + d
        os.path.walk(tmpth, finddir, 0)



#获取一个路径中所包含的所有目录及子目录
def getAllLevelDirs(dirpths):
    dirleves = []
    dirtmp = ''
    for d in dirpths:
        dirtmp += '/' + d
        dirleves.append(dirtmp)
    return dirleves

#在outpth目录下创建ndir路径中的所有目录，是否使用决对路径
def makeDir(outpth,ndir):
    tmpdir = ''
    if ndir[0] == '/':
        tmpdir = outpth + ndir
    else:
        tmpdir = outpth + '/' + ndir
    print tmpdir
    if not os.path.exists(tmpdir):
        os.mkdir(tmpdir)

# 创建一个目录下的所有子目录到另一个目录
def createDirs(spth,tpth):
    files = getAllExtFile(spth,'.*')
    makedirstmp = []
    isOK = True
    # 分析所有要创建的目录
    tmpfpth = fpth
    for d in files:
        if d[1] != '/' and (not d[1] in makedirstmp): #创建未创建的目录层级
            tmpdir = d[1][1:]
            tmpleves = tmpdir.split('/')
            alldirs = getAllLevelDirs(tmpleves)
            for dtmp in alldirs:
                if not dtmp in makedirstmp:
                    makeDir(tpth,dtmp)
                    makedirstmp.append(dtmp)

# 替换文件名
def replaceFileName(path,sname,replaceStr,tostr):
    a = sname
    tmpname = a.replace(replaceStr, tostr)
    outpath = path + tmpname
    oldpath = path + sname
    cmd = "mv %s %s"%(oldpath,outpath)
    print cmd
    os.system("mv %s %s"%(oldpath,outpath))

# 替换目录下的文件名中某个字符串为其他字符串
def renameDir(sdir,replacestr,tostr,exittype):
    files = getAllExtFile(sdir,fromatx = exittype)
    allfilepath = []
    for f in files:
        tmppath = sdir + f[1]
        filename = f[2] + exittype
        allfilepath.append([tmppath,filename])
    for p in allfilepath:
        replaceFileName(p[0], p[1], replacestr, tostr)

def conventWavToMp3(pth,outpth):
	if os.path.exists(outpth):
		cmd = 'rm -r %s'%(outpth)
		os.system(cmd)
	cmd = 'mkdir %s'%(outpth)
	os.system(cmd)
	createDirs(pth, outpth)
	if os.path.exists(pth):
		removeProjectAllHideDir(pth)
	allfiles = getAllFiles(pth)
	for fp in allfiles:
		fpth = pth + fp
		name,text = os.path.splitext(fp)
		if cmp(text.lower(), '.wav') == 0:
			outfth = outpth + name + '.mp3'
			cmd = 'ffmpeg -i %s -acodec libmp3lame %s'%(fpth,outfth) #电脑需要安装ffmpeg库,mac下使用brew install ffmpeg来安装
			os.system(cmd)
			print '已转换:',fp
		else:
			outfth = outpth + fp
			cmd = 'cp %s %s'%(fpth,outfth)
			os.system(cmd)
			print '复制文件:',fp
#测试
if __name__ == '__main__':
    args = sys.argv
    fpth = ''
    outpth = ''
    if len(args) == 2 :
    	if os.path.exists(args[1]):
            fpth = args[1]
            name,text = os.path.split(fpth)
            outpth = name + os.sep + 'out'
            print '开始转换'
            print fpth
            print '目录下所有wav文件为mp3格式,其他文件只复制不作处理'
            print '转换后输出到:',outpth
            name,text = os.path.split(fpth)
            print name,text
            conventWavToMp3(fpth,outpth)
        else:
            print "请加上要转码的文件目录路径,未加输出路径则默认输出到out目录"
    elif len(args) == 3 :
        if os.path.exists(args[1]):
            fpth = args[1]
            outpth = args[2]
            if outpth.find('/') != -1 or outpth.find('\\') != -1:
            	outpth = outpth
            else:
            	name,text = os.path.split(fpth)
            	outpth = name + os.sep + outpth
            print '开始转换'
            print fpth
            print '目录下所有wav文件为mp3格式,其他文件只复制不作处理'
            print '转换后输出到:',outpth
            conventWavToMp3(fpth,outpth)
        else:
            print "请加上要转码的文件目录路径,未加输出路径则默认输出到out目录"
    else:
        print "请加上要转码的文件路径"

    