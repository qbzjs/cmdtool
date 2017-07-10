#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-03-24 17:43:22
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$
# 内部测试版更新版本文件上传脚本
import os
import sys
from ftplib import FTP
import ftplib


projectPth = '/Users/user/doc/shanghai/projecte/shanghai/shanghai_debug'
ftpUpdatePth = '/mahjong_shanghai_test/update'
ftpUpdateShanghai = '/mahjong_shanghai_test'

# 字节bytes转化kb\m\g
def formatSize(bytes):
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except:
        print("传入的字节格式不对")
        return "Error"

    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return "%fG" % (G)
        else:
            return "%fM" % (M)
    else:
        return "%fkb" % (kb)

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

#获取所有界面的json文件列表
def getAllExtFile(pth,fromatx = ".erl"):
    jsondir = pth
    jsonfilelist = []
    for root, _dirs, files in os.walk(jsondir):
        for filex in files:          
            #print filex
            name,text = os.path.splitext(filex)
            if name == '.DS_Store': #mac下的系统文件
                continue
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





class FTPTool():
    """docstring for FTPTool"""
    def __init__(self, ftpIP = "ip地址",ftpPort = "21",userNname = "username",userPW = "password",defPth = "/ftppath"):
        self.ftp = FTP() 
        self.ftpIP = ftpIP          #ftp服务器ip
        self.ftpPort = ftpPort      #ftp服务器端口
        self.ftpRootPth = defPth     #远程根路径
        self.ftpPth = defPth         #当前服务器路径
        self.userName = userNname
        self.userPW = userPW
        self.bufsize = 4096                      #设置的缓冲区大小
        self.initFTPServer()
        self._is_dir = False
    def initFTPServer(self):
        self.ftp.set_debuglevel(0)
        self.ftp.connect(self.ftpIP,self.ftpPort)          #连接的ftp sever和端口
        self.ftp.login(self.userName,self.userPW)      #连接的用户名，密码
        # print self.ftp.getwelcome()  # 获得欢迎信息  
        
    def addPth(self,pth):
        return self.ftpPth + '/' + pth2

    #获取所有可能级别的目录层
    def getAllLevelDirs(self,dirpths):
        dirleves = []
        dirtmp = ''
        for d in dirpths:
            dirtmp += '/' + d
            dirleves.append(dirtmp)
        return dirleves

    #上传目录到ftp服务器指定目录下,上传完成时调用通知回调,isOverWrite是否覆盖,默认覆盖
    def updateDirToServer(self,localDir,serverPth,upendCallBack,isOverWrite = True):
        _localfpth,fpth = os.path.split(localDir)
        self.setFtpServerPath(serverPth)
        self.makeFtpDir(fpth)
        self.setFtpServerPath(serverPth + '/' + fpth)
        # localfpth = '/Users/junpengzhang/doc/shanghai/projecte/test/mahjong_shanghai_test/10847/src'
        files = getAllExtFile(localDir,'.*')
        makedirs = []
        isOK = True
        # 分析所有要创建的目录
        count = len(files)
        print "总上传%s目录中文件数:%d"%(fpth,count)
        tmpfpth = fpth
        for d in files:
            if d[1] != '/' and (not d[1] in makedirs): #创建未创建的目录层级
                tmpdir = d[1][1:]
                tmpleves = tmpdir.split('/')
                alldirs = self.getAllLevelDirs(tmpleves)
                for dtmp in alldirs:
                    if not dtmp in makedirs:
                        self.makeFtpDir(dtmp)
                        makedirs.append(dtmp)
            lpth = localDir + d[0]
            fpth = self.ftpPth + d[0]
            isOK = self.updateFileToServer(lpth, fpth)
            if isOK :
                print "(%d)剩余文件,目录%s上传文件完成:%s"%(count,tmpfpth,d[0][1:])
                count -= 1
            else:
                print "文件上传大小错误:%s"%(d[0][1:])
        outstr = "目录%s上传结果:%d"%(fpth,isOK)
        upendCallBack(outstr)

    #创建ftp服务器目录，是否使用服务器决对路径
    def makeFtpDir(self,ndir,isTruePath = False):
        tmpdir = ''
        if ndir[0] == '/':
            tmpdir = self.ftpPth + ndir
        else:
            tmpdir = self.ftpPth + '/' + ndir
        print tmpdir
        if not self.isFtpPath(tmpdir):
            self.ftp.mkd(tmpdir)
        else:
            print "服务器已存在目录:%s"%(tmpdir)


    #上传文件到ftp服务器指定目录下isOverWrite是否覆盖,默认覆盖
    def updateFileToServer(self,localFile,serverPth,isOverWrite = True):
        # print localFile,'===>',serverPth
        command = 'STOR ' + serverPth
        filehandler = open(localFile,'rb')
        self.ftp.storbinary(command,filehandler,self.bufsize)
        filehandler.close()
        lsize = self.getLocalFileSize(localFile)
        fsize = self.getServerFileSize(serverPth)
        if lsize == fsize :
            return True
        else:
            return False

    #检测上传文件大小以确定是否上传完成
    def checkUpload(self,localPth,serverPth):
        pass

    #列出服务器路径下的目录
    def getListServerDir(self,serverPth):
        print self.ftp.dir()
        self.ftp.cwd(serverPth)
        return self.ftp.nlst()

    #列出服务器路径下的文件
    def getListServerPathFiles(self,serverPth):
        self.ftp.cwd(serverPth)
        return self.ftp.nlst()

    #获取服务器文件大小
    def getServerFileSize(self,serverFilePth):
        # print serverFilePth
        return self.ftp.size(serverFilePth)

    #获取本地文件大小
    def getLocalFileSize(self,localFilePth):
        try:
            psize = os.path.getsize(localFilePth)
            return psize
        except Exception as err:
            print(err)

    #打开调试级别2，显示详细信息,0,关闭
    def setDebugLeve(self,level):
        self.ftp.set_debuglevel(level)
    #退出ftp
    def quit(self):
        self.ftp.quit()

    #设置远程ftp路径
    def setFtpServerPath(self,ftpPath):
        print ftpPath
        self.ftp.cwd(ftpPath)

        self.ftpPth = ftpPath
        print '设置远程ftp目录:%s'%(ftpPath)

    #远程是否有此路径
    def isFtpPath(self,ftp_filepth):
        try:
            if ftp_filepth in self.ftp.nlst(os.path.dirname(ftp_filepth)):
                return True
            else:
                return False
        except ftplib.error_perm,e:
            return False
    #创建新版本目录
    def createNewVisionDir(self):
        updatepth = '/ftppath/update'
        nlist = self.getListServerPathFiles(updatepth)
        nlist.sort(reverse=True)
        print nlist
        vnlist = self.getListServerPathFiles(updatepth + '/' + nlist[0])
        print vnlist
        nversiondir = ''
        if 'res' in vnlist and 'src_et' in vnlist :
            nversiondir = str(int(nlist[0])+1)
        if nversiondir :
            print "在ftp服务器上海测试项目update目录下创建新版本目录:%s"%(nversiondir)
            self.ftp.cwd(updatepth)
            self.ftp.mkd(nversiondir)
            nlist = self.getListServerPathFiles(updatepth)
            nlist.sort(reverse=True)
            print nlist
            if nlist[0] == nversiondir :
                return nversiondir
            else:
                print "创建远程目录%s出现错误"%(nversiondir)
        else:
            print "新版本目录已存在:%s,将使用ftp服务器上的此目录作为新版本目录"%(nlist[0])
            nversiondir = nlist[0]
        return nversiondir

    def getLastVersionID(self):
        updatepth = '/ftppath/update'
        nlist = self.getListServerPathFiles(updatepth)
        nlist.sort(reverse=True)
        print nlist[0]
    #回调函数
    def _ftp_list(self, line):
        print line
        list = line.split(' ')
        if self.ftp_dir_name==list[-1] and list[0].startswith('d'):
            self._is_dir = True
     
    def is_ftp_dir(self,ftp_path):
        ftp_path = ftp_path.rstrip('/')
        ftp_parent_path = os.path.dirname(ftp_path)
        self.ftp_dir_name = os.path.basename(ftp_path)
        self._is_dir = False
        if ftp_path == '.' or ftp_path== './' or ftp_path=='':
            self._is_dir = True
        else:
            print "yyy"
            try:
                #下边的两个方法都可以
                # self.ftp.retrlines('LIST %s' %ftp_parent_path,self._ftp_list)
                self.ftp.dir(ftp_parent_path,self._ftp_list)
            except ftplib.error_perm,e:
                return self._is_dir       
        return self._is_dir



#修改本脚本配制文件
def changeCreatePythonVersion(versionNumber):
    strversionnum = str(versionNumber)
    vernumber = int(strversionnum) - 10000
    testconfpth = projectPth + '/assetsUpdate_test/configAssetsUpdate.py'
    f = open(testconfpth,'r')
    pylines = f.readlines()
    f.close()
    for ln in range(len(pylines)):
        l = pylines[ln]
        if l.find('VersionNumber = "') != -1 :
            pylines[ln] = 'VersionNumber = "1.0.%d"\n'%(vernumber)
        if l.find('VersionString = "') != -1 :
            pylines[ln] = 'VersionString = "%s"\n'%(strversionnum)
    outstr = ''
    for l in pylines:
        outstr += l
    f = open(testconfpth,'w')
    f.write(outstr)
    f.close()

#获取本地上传文件目录
def getLocalUploadDir(pdarpth):
    dirs = os.listdir(pdarpth)
    if '.DS_Store' in dirs:
        dirs.remove('.DS_Store')
    dirs.sort(reverse=True)
    return pdarpth + '/' + dirs[0]

def uploadDirCallback(backdat):
    print "上传文件结束"
    print backdat

#上传新测试版本
def uploadNewVersionData(localpth):
    _fpth,localnumber = os.path.split(localpth)
    ftptool = FTPTool()
    ftptool.setDebugLeve(0)
    nversiondir = ftptool.createNewVisionDir()
    ftppath = ftpUpdatePth + '/' + localnumber
    if nversiondir == localnumber :
        print "本地与服务器文件版设置正常，可以上传文件"
    else:
        print "本地目录与服务器目录不同"
        if ftptool.isFtpPath(ftpUpdatePth + '/' + localnumber):
            print "服务器目录中已有res或src_et目录,将使用复盖方式上传"
        else:
            print '服务器没有相应版本目录，上传错误'
            return
    print "上传src_et"
    ftptool.updateDirToServer(localpth + '/src_et',ftppath,uploadDirCallback)
    print "上传res"
    ftptool.updateDirToServer(localpth + '/res',ftppath,uploadDirCallback)
    print "上传版本控制文件project.manifest"
    ftptool.updateFileToServer(localpth + '/project.manifest', ftpUpdateShanghai + '/project.manifest')
    print "上传版控制文件version.manifest"
    ftptool.updateFileToServer(localpth + '/version.manifest', ftpUpdateShanghai + '/version.manifest')

    print "上海客户端,测试服热更新,版本%s"%(localnumber)

if __name__ == '__main__':
    args = sys.argv
    fpth = ''
    if len(args) == 2 :
        if args[1] == 'createdir':
            ftptool = FTPTool()
            ftptool.setDebugLeve(0)
            nversiondir = ftptool.createNewVisionDir()
            changeCreatePythonVersion(nversiondir)
            print "服务器新版本目录创建完成:%s"%(nversiondir)
            print "本地脚本配置文件修改完成"
        elif args[1] == 'LastVersionID':
            ftptool = FTPTool()
            ftptool.setDebugLeve(0)
            ftptool.getLastVersionID()

    elif len(args) == 3 and args[1] == 'upload':
        localPath = args[2]
        print "本地上传文件保存路径:%s"%(localPath)
        ldir = getLocalUploadDir(localPath)
        print "本地上传到ftp的新版本生成文件目录:%s"%(ldir)
        uploadNewVersionData(ldir)

    # ftptool = FTPTool()
    # ftptool.setDebugLeve(0)
    # ftptool.ftp.cwd('/mahjong_shanghai_test/update/10848')
    # localFile = "/Users/junpengzhang/doc/shanghai/projecte/test/mahjong_shanghai_test/10847/src_et/main.luac"
    # serverPth = "/mahjong_shanghai_test/update/10848/main.luac"
    # # ftptool.updateFileToServer(localFile, serverPth)
    # # command = 'STOR ' + serverPth
    # # filehandler = open(localFile,'rb')
    # # ftptool.ftp.storbinary(command,filehandler,ftptool.bufsize)
    # # filehandler.close()
    # ftptool.updateDirToServer('/Users/junpengzhang/doc/shanghai/projecte/test/mahjong_shanghai_test/10847/src_et','/mahjong_shanghai_test/update/10848',uploadDirCallback)
    # print ftptool.getAllLevelDirs(['a','b','c'])
    # print ftptool.is_ftpPath('/mahjong_shanghai_test/update')
    # print ftptool.is_ftp_dir('/mahjong_shanghai_test/version.manifest')
# ftp=FTP()                         #设置变量
# ftp.set_debuglevel(2)             #打开调试级别2，显示详细信息
# # print ftp.getwelcome()            #打印出欢迎信息
# # ftp.sendcmd("TYPE i")    # Switch to Binary mode
# # Get size of file
# fsize =  ftp.size("/mahjong_shanghai_test/update/10837/src_et/main.luac")
# print fsize
# ftp.set_debuglevel(0)             #关闭调试模式
# ftp.quit()                        #退出ftp