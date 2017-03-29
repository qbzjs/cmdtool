#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-02-22 09:44:42

import datetime  
import email  
import smtplib  
import os  
import sys
from email.mime.text import MIMEText  
from email.mime.multipart import MIMEMultipart  

  
class MyEmail:  
    def __init__(self):  
        self.confilepth = 'mail.conf'
        self.user = ""    		#你的邮件地址
        self.passwd = ""  	#你的邮箱密码
        self.to_list = []  		#收件人列表
        self.cc_list = []  		#抄送人列表
        self.tag = None  	#邮件标题
        self.doc = None  	#邮件附件
        self.initAccount()	#我这里使用的是配制文件初始化上的上边参数
    def initAccount(self):
        f = open('mail.conf')
        tmps = f.readlines()
        f.close()
        self.user = tmps[0]
        self.passwd = tmps[1]
        if len(tmps) > 2:
            self.to_list = tmps[2].split(',')
        if len(tmps) > 3:
            self.cc_list = tmps[3].split(',')
    def send(self,ttag,ttext):  
        ''''' 
        发送邮件 
        '''  
        self.tag = ttag
        try:  
            server = smtplib.SMTP_SSL("smtp.exmail.qq.com",port=465)  
            server.login(self.user,self.passwd)  
            server.sendmail(self.user, self.to_list + self.cc_list, self.get_attach(ttext))  
            server.close()  
            print "send email successful"  
        except Exception,e:  
            ortstr = conventStrTOUtf8(str(e))
            print ortstr
            print "send email failed"  
    def get_attach(self,ttext):  
        ''''' 
        构造邮件内容 
        '''  
        attach = MIMEMultipart('related')  
        #添加邮件内容  
        txt = MIMEText(ttext)  
        attach.attach(txt)  
        if self.tag is not None:  
            #主题,最上面的一行  
            attach["Subject"] = self.tag  
        if self.user is not None:  
            #显示在发件人  
            attach["From"] = "zhangjunpeng<%s>"%self.user  
        if self.to_list:  
            #收件人列表  
            attach["To"] = ",".join(self.to_list)  
        if self.cc_list:  
            #抄送列表  
            attach["Cc"] = ",".join(self.cc_list)  
        if self.doc:  
            pass
            #估计任何文件都可以用base64，比如rar等  
            #文件名汉字用gbk编码代替  
            # name = os.path.basename(self.doc).encode("gbk")  
            # f = open(self.doc,"rb")  
            # doc = MIMEText('填写邮件内容','plain','utf-8')
            # doc["Content-Type"] = 'application/octet-stream'  
            # doc["Content-Disposition"] = 'attachment; filename="'+name+'"'  
            # attach.attach(doc)  
            # f.close()  
        return attach.as_string()  

if __name__=="__main__":  
    args = sys.argv
    if len(args) == 3:
        my = MyEmail()  
        tag = args[1]     #邮件标题  
        context = args[2]   #邮件内容
        my.send(tag,context) 
    else:
        print "发邮件参数错误,第一个参数:标题,第二个参数:邮件内容"

