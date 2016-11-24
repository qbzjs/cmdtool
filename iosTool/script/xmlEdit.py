#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys


# def main():
# 	s1 = 'abcdaa123axjfielsfjei123'
# 	print s1.find('123')
# 	print s1.rfind('123')
# 	print s1[:s1.rfind('123')]

# if __name__ == '__main__':
# 	main()

allstr = '''	<key>NSCameraUsageDescription</key>
    <string>cameraDesciption</string>
    <key>NSMicrophoneUsageDescription</key>
    <string>microphoneDesciption</string>
    <key>NSPhotoLibraryUsageDescription</key>
    <string>photoLibraryDesciption</string>
'''
keycam = '''	<key>NSCameraUsageDescription</key>
    <string>cameraDesciption</string>
'''
keymic = '''    <key>NSMicrophoneUsageDescription</key>
    <string>microphoneDesciption</string>
'''
keyphoto = '''    <key>NSPhotoLibraryUsageDescription</key>
    <string>photoLibraryDesciption</string>
'''


def addKey(xmlpth):
	f = open(xmlpth,'r')
	xmldat = f.read()
	f.close()
	ln = xmldat.rfind('</dict>')
	addstr = ''
	if xmldat.find('NSCameraUsageDescription') == -1:
		addstr += keycam
	if xmldat.find('NSMicrophoneUsageDescription') == -1:
		addstr += keymic
	if xmldat.find('NSPhotoLibraryUsageDescription') == -1;
		addstr += keyphoto
	out = xmldat[:ln] + addstr + xmldat[ln:]
	f = open(xmlpth,'w')
	f.write(out)
	f.close()

if __name__ == '__main__':
	args = sys.argv
	xmlpth = ''
	if len(args) == 2:
		xmlpth = args[1]	#Info.plist路径
		addKey(xmlpth)
	else:
		print 'Info.plist文件路径参数错误'