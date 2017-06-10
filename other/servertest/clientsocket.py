#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-06-10 10:52:54
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
import socket
import base64
import sys


myname = socket.getfqdn(socket.gethostname())
myaddr = socket.gethostbyname(myname)

ipaddr = '172.16.81.29'
port = 9102
conftest = 'matchconf.ini'
confused = 'match_info_config.ini'

def readMatchConfig(roomid,ucount):

    f = open(conftest,'r')
    datastr = f.read()
    strtmp = 'MatchId = %d'%(roomid)
    datastr = datastr.replace('MatchId = 333333',strtmp)
    strtmp = 'RotateCount = %d'%(ucount)
    datastr = datastr.replace('RotateCount = 3',strtmp)
    f.close()
    fs = open(confused,'w')
    fs.write(datastr)
    fs.close()
    outbase64str = base64.b64encode(datastr)
    return outbase64str

def setMatchConfig(roomid,ucount):
	#链接服务端ip和端口
	ip_port = (ipaddr,port)
	#生成一个句柄
	sk = socket.socket()
	#请求连接服务端
	sk.connect(ip_port)
	#发送数据
	outbase64 = readMatchConfig(roomid,ucount)
	sk.sendall(outbase64)
	#接受数据
	server_reply = sk.recv(1024)
	#打印接受的数据
	print (server_reply)
	#关闭连接
	sk.close()

if __name__ == '__main__':
    args = sys.argv
    roomID = 0
    ucount = 3
    if len(args) == 2 :
        if len(args[1]) == 6:
            roomID = int(args[1])
            ucount = 3
        else:
            print "输入的房间号位数不对,要求是6位数字"
    elif len(args) == 3:
    	if len(args[1]) == 6 and len(args[2]) <= 3:
            roomID = int(args[1])
            ucount = int(args[2])
        else:
            print "输入的房间号位数不对,要求是6位数字,人数不能大于3位数"
    elif len(args) == 1:
    	roomID = 222222
        ucount = 3
    else:
    	print "输入参数错误"

    if roomID != 0 :
        print '房间号:',roomID
        print '房间人数:',ucount
        setMatchConfig(roomID, ucount)