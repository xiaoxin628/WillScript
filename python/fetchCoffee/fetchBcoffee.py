#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#Filename : fetchBcoffee.py
#Author   :   Will
#Email   :   lishuzu@gmail.com
import MySQLdb
import lxml.html, lxml.etree
import sys, os, urllib, urllib2, cookielib, Cookie, datetime, time, re, socket
reload(sys)
sys.setdefaultencoding("utf-8")
socket.setdefaulttimeout(3600)
#Config
timeOut = 99999
categoryList = {
	'coffeenews':{'catid':1, 'page':15},
	'cafenews':{'catid':2, 'page':7},
	'study':{'catid':3, 'page':13},
	'chandi':{'catid':4, 'page':2},
}
#db
C = DB = ''
#lib
def dbConnect():
		global DB, C
		DB = MySQLdb.Connect(host="localhost",user='root', passwd="lishuzu511",db="timepic",charset="utf8")
		C = DB.cursor(MySQLdb.cursors.DictCursor)

def fetchLog(logstr):
	if logstr:
		file_object = open('bcoffee.log', 'a+')
		file_object.write(logstr+"\r\n")
		file_object.close()
		return True
	return False

def fetchPage(url, catid):
		targetUrl = url
		try:
			pageHtml = opener.open(targetUrl, timeout=timeOut).read()
			htmlString = lxml.html.fromstring(pageHtml)
			coffeeArticls = htmlString.xpath("//ul[@class='newslist']/li")
			total = len(coffeeArticls)
			for	items in coffeeArticls:
				articlUrl = items.xpath("./h2/a")[0].get('href')
				C.execute("SELECT * from tp_coffee_article WHERE source = %s", articlUrl)
				isexist=C.fetchone()
				if isexist == None:
					articlPage = opener.open(articlUrl, timeout=timeOut).read().decode("utf-8", "ignore")
					articlPage = lxml.html.fromstring(articlPage)
					title = articlPage.xpath("//div[@class='single page']/h2")[0].text_content()
					content = articlPage.xpath("//div[@class='entrycontent']")[0].text_content()
					query = C.execute("INSERT INTO  tp_coffee_article(title, content, catid, dateline, tag, source) VALUES(%s, %s, %s, %s, %s, %s)", (title, content, catid, int(time.time()), "", articlUrl))
					print "url:"+articlUrl
					print "[%s]title:%s [%s]" %(total ,title, query)
				else:
					print "[%s is exist!]url:%s" %(total,articlUrl)
				total -= 1
				#print "content:"+content
				#fetchLog("url:"+articlUrl)
				#fetchLog("title:"+title)
				#fetchLog("content:"+content)
		except urllib2.HTTPError, error:
				contents = error.read()
				print contents
				exit()

#main
dbConnect()
bcoffeeCookie = cookielib.CookieJar()
siteCookie = urllib2.HTTPCookieProcessor(bcoffeeCookie)
opener = urllib2.build_opener(siteCookie)	
opener.addheaders = [
		('User-Agent','Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html) '),
		('Referer','http://bcoffee.cn'),
		('Content-Type','text/html'),
		('Accept-Charset','UTF-8'),
]
urllib2.install_opener(opener)
for cat,value in categoryList.items():
		print cat
		for i in range(1,value['page']+1):
			targetUrl = 'http://www.bcoffee.cn/cat/coffee/'+cat+'/page/'+str(i)
			print targetUrl
			fetchPage(targetUrl, value['catid'])

