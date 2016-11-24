#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-11-10 11:28:17
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import paramiko
import pexpect
import pinyin
import os
import sys

dattmp = [0,1]

def getBIDFromString(pstr):
	bidtmp = pstr[pstr.find('<')+1:pstr.find('>')]
	return bidtmp

def findAppBID(apps,appname):
	lineapps = apps
	numtmps = ['1','2','3','4','5','6','7','8','9']
	appBID = ''
	for l in lineapps:
		if len(l) >3:
			tmpstr = l[0]
			if tmpstr in numtmps:
				if l.find(appname) != -1:
					appBID = getBIDFromString(l)
	if appBID:
		f = open('allbid.txt','a')
		f.write(appname + ',' + appBID + '\n')
		f.close()
	return appBID

def gtUTF8Str(outx):
	out = outx.readlines()
	appsx = []
	for o in out:
		tmpstr = o.encode('utf-8')[:-1]
		print tmpstr
		appsx.append(tmpstr)
	return appsx

#获取手机上脱壳后的ipa地址
def getFileiPhonePth(outstrs):
	ox = ''
	for t in outstrs:
		if t[:4] == 'DONE':
			ox = t[t.find('/'):]
	print ox
	return ox


def ssh_cmd(ip,passwd,cmd):
    ret = -1
    print cmd
    xtmp = 'scp -p root@%s:%s'%(ip,cmd)
    print xtmp
    ssh = pexpect.spawn(xtmp)
    try:
        i = ssh.expect(['*password:', 'continue connecting (yes/no)?'], timeout=0)
        if i == 0 :
            ssh.sendline(passwd)
        elif i == 1:
            ssh.sendline('yes\n')
            ssh.expect('*password:')
            ssh.sendline(passwd)
        #ssh.sendline(xtmp)
        r = ssh.read()
        print r
        ssh.close()
        ret = 0
    except pexpect.EOF:
        print "EOF"
        ssh.close()
        ret = -1
    except pexpect.TIMEOUT:
        print "TIMEOUT"
        ssh.close()
        ret = -2
    return ret 


def downcallback(size, file_size):
	olds = (float(dattmp[0])/float(dattmp[1]))*100
	nlds = (float(size)/float(file_size))*100
	if nlds - olds >= 0.1:
		dattmp[0] = size
		dattmp[1] = file_size
		print 'download:%.2f%%'%(nlds)

#从手机下载脱壳后的ipa包到本地,反回本地ipa包相对路径
def downloadIpaFromiPhone(fpth,ssh):
	print '开始下载脱壳后ipa到手机'
	_pth,fname = os.path.split(fpth)
	sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
	sftp = ssh.open_sftp()
	sftp.get(fpth,fname,callback=downcallback)
	print '脱壳后ipa下载文件结束'
	return fname


#中文转首字母大写英文
def getStringName(hanyu):
	pname = pinyin.get_initial(hanyu,delimiter='').upper()
	print pname
	return pname

#获了新名字
def changeName(fpth,appname):
	tmpth = ''
	nname = getStringName(appname)
	a,b = os.path.split(fpth)
	tmpth = a + '/' + nname + '.ipa'
	return tmpth

#app脱壳,返回脱壳后的ipa手机地址
def ssh2ClutchApp(tip,username,passwd,appname):
   	try:
   		paramiko.util.log_to_file("filename.log")
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		print 'xxxx1'
		ssh.connect(tip,22,username,passwd,timeout=5)
		print 'xxxx2'
		stdin, stdout, stderr = ssh.exec_command('Clutch -i')
		print appname
		BID = findAppBID(gtUTF8Str(stdout),appname)
		print BID
		if BID:
			cmd = 'Clutch -d ' + BID
			print cmd
			stdin, stdout, stderr = ssh.exec_command(cmd)
			print 'Clutch -d',stderr.read()
			if stderr.read() == '':
				print '开始脱壳'
			ipapth = getFileiPhonePth(gtUTF8Str(stdout))
			cnamepth = changeName(ipapth,appname)
			cmd = 'mv "' + ipapth + '" ' + cnamepth
			print cmd
			print '对况壳后ipa文件重命名'
			stdin,stdout,stderr = ssh.exec_command(cmd)
			print 'mv',stderr.read()
			if stderr.read() == '':
				print '重命名完成'
			return cnamepth,ssh
		else:
			print '手机(%s)没有找到<%s>应用'%(tip,appname)
			return ''
		ssh.close()
	except :
		print E
		print '%s\tError\n'%(tip)
	return '',None

def ssh2ClutchApp(tip,username,passwd,appname):
	if True:
   		paramiko.util.log_to_file("filename.log")
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		print 'xxxx1'
		ssh.connect(tip,22,username,passwd,timeout=5)
		print 'xxxx2'
		stdin, stdout, stderr = ssh.exec_command('Clutch -i')
		print appname
		BID = findAppBID(gtUTF8Str(stdout),appname)
		print BID
		if BID:
			cmd = 'Clutch -d ' + BID
			print cmd
			stdin, stdout, stderr = ssh.exec_command(cmd)
			print 'Clutch -d',stderr.read()
			if stderr.read() == '':
				print '开始脱壳'
			ipapth = getFileiPhonePth(gtUTF8Str(stdout))
			cnamepth = changeName(ipapth,appname)
			cmd = 'mv "' + ipapth + '" ' + cnamepth
			print cmd
			print '对况壳后ipa文件重命名'
			stdin,stdout,stderr = ssh.exec_command(cmd)
			print 'mv',stderr.read()
			if stderr.read() == '':
				print '重命名完成'
			return cnamepth,ssh
		else:
			print '手机(%s)没有找到<%s>应用'%(tip,appname)
			return ''
		ssh.close()
	else :
		print E
		print '%s\tError\n'%(tip)
	return '',None



if __name__=='__main__':
	args = sys.argv
	ip = '172.16.80.193'	#手机ip地址
	username = "root"  		#用户名
	passwd = "123456"    	#密码
	appname = '音乐与弹幕社交'
	if len(args) > 4:
		ip = args[1]
		username = args[2]
		passwd = args[3]
		appname = args[4]
	localname = getStringName(appname)
	print '开始在手机上查找名子中有<%s>的app，并试着进行脱壳'%(appname)
	print ip,username,passwd,appname
	iphonepth,ssh = ssh2ClutchApp(ip,username,passwd,appname)
	if iphonepth:
		print '<'+ appname +'>脱壳成功，ipa文件在手机位置:'
		print iphonepth
		lfpth = downloadIpaFromiPhone(iphonepth,ssh)
		print lfpth
	else:
		print '脱壳失败'
    