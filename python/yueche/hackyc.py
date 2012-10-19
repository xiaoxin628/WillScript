#!/usr/bin/python
#coding:utf-8
#Filename : hackyueche.py
#Author   :   Will

import lxml.html, lxml.etree
import sys, os, urllib, urllib2, cookielib, Cookie, datetime, time, json, md5, re, cPickle, random
from config import *
reload(sys)
sys.setdefaultencoding("utf-8")
if len(sys.argv)<2:
	print "./hackyuecheV2.py will"
	print "will 是config中的配置项，请配置相关用户名和密码"
	exit()
#Config
#是否输出到屏幕 1为输出 0则输出到当前目录下的日志中
user = sys.argv[1]
targetUrl = 'http://haijia.bjxueche.net/login.aspx'
username = users[user]['username']
password = users[user]['password']
rDate = users[user]['date']
reserveDate = ""
reserveTime = ""
logPath = sys.path[0]+"/"

postCookie = {
	'txtIMGCode':'hukv',#定义验证码 每次都用同一个验证码
	'ImgCode':'Q73fsrhw+VE=',
	'txtBookingCode':'pj71',
	'BookingCode':'srs1T66YBYl8c+HCL4WZDi1tEhoiyj/YR2YNhGt0fwV6csMjKJ3gyw==',
}

reserveTimeData = {
	'morning':'812',
	'afternoon':'15',
	'night':'58',
}

todayYear = str(datetime.date.today().year)

carList = []
#COOKIE
wcookie = cookielib.MozillaCookieJar('./wcookie.txt')
wcookie.set_cookie(cookielib.Cookie(version=0, name='ImgCode', value=postCookie['ImgCode'], port=None, port_specified=False, domain='haijia.bjxueche.net', domain_specified=False, domain_initial_dot=False, path='/', path_specified=True, secure=None, expires=(int(time.time())+3600*24*30), discard=False, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False))
wcookie.set_cookie(cookielib.Cookie(version=0, name='BookingCode', value=postCookie['BookingCode'], port=None, port_specified=False, domain='haijia.bjxueche.net', domain_specified=False, domain_initial_dot=False, path='/', path_specified=True, secure=None, expires=(int(time.time())+3600*24*30), discard=False, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False))
siteCookie = urllib2.HTTPCookieProcessor(wcookie)
opener = urllib2.build_opener(siteCookie)	

opener.addheaders = [
        ('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:14.0) Gecko/20100101 Firefox/14.0.1 '),
        ('Referer','http://haijia.bjxueche.net'),
        ('Content-Type','text/html'),
        ('Accept-Charset','UTF-8'),
]

urllib2.install_opener(opener)
	

def setCookie():
	global opener, wcookie
#开始登录海驾约车网站
def hjLogin(username,password,url):
	postData = {
		'BtnLogin':'登 录',
		'__VIEWSTATE':'/wEPDwUKMTg0NDI4MDE5OGRkecATcwUaw2gw+8bwppLpsBEl2Scfh8acL+X+ssZCx+s=',
		'__EVENTVALIDATION':'/wEWBgKIhaiLCwKl1bKzCQK1qbSRCwLoyMm8DwLi44eGDAKAv7D9CmpaYpLSv4GbTlgEhWMl7ZXk+dc5ORysip3DOr8h9FQP',
		'txtUserName':username,
		'txtPassword':password,
		'rcode':'',
		'txtIMGCode':postCookie['txtIMGCode'],
	}
	setCookie()
	req = urllib2.Request(targetUrl, urllib.urlencode(postData))

	runLog = username+' start login..'
	errorLog(runLog)
	try:
			htmldoc = opener.open(req, timeout=timeOut).read()
			htmldoc = htmldoc.decode("utf-8", "ignore")
			if htmldoc.find('ych2.aspx') != -1:
				runLog =  'username: '+username+'  login sucessful!'
				errorLog(runLog)
				findButton()
			else:
				htmlString = lxml.html.fromstring(htmldoc)
				recodetext = htmlString.xpath("//form/script")[0].text_content().replace('alert', '', 1)
				runLog = recodetext
				errorLog(runLog)
	except urllib2.HTTPError, error:
			contents = error.read()
			runLog = contents
			errorLog(runLog)
	except  urllib2.URLError, error:
			runLog = "error:",  error.reason
			errorLog(runLog)
	except:
		import traceback,sys
		runLog="".join(traceback.format_exception(*sys.exc_info()))
		errorLog(runLog)
		print "Oh, we got a problem!"

def findButton():
	waitTime()
	targetUrl = 'http://haijia.bjxueche.net/ych2.aspx'
	try:
		runLog = "check left reserve time..."
		errorLog(runLog)
		htmldoc = opener.open(targetUrl, timeout=timeOut).read()
		htmldoc = htmldoc.decode("utf-8", "ignore")
		htmlString = lxml.html.fromstring(htmldoc)
		#循环取出要预约的日期
		if len(rDate) >= 1: 
			for dateItem in rDate:
				leftTime = ''
				reserveDate = todayYear+dateItem[0]
				reserveTime = dateItem[1]
				searchDate = reserveDate
				searchTime = reserveTimeData[reserveTime]
				rule = "//td[@yyrq='"+searchDate+"' and @yysd='"+searchTime+"']"
				chooseDate = htmlString.xpath(rule)
				if chooseDate:
					leftTime = chooseDate[0].text.strip()
					if leftTime >= 0 and leftTime != '无' and leftTime != '已约':
						runLog = "date: %s %s times:%s" % (searchDate, searchTime, leftTime)
						errorLog(runLog)
						getCars(searchDate, searchTime)
					else:
						runLog = "date: %s %s times:%s" % (searchDate, searchTime, leftTime)
						runLog = "Sorry! %s %s The left time is %s" % (searchDate, searchTime, leftTime)
						errorLog(runLog)
				else:
					bookTime =  time.mktime(time.strptime(reserveDate,'%Y%m%d'))
					expiredTime =  int(time.time())+3600*24*7
					#print time.strftime("%Y-%m-%d ", time.localtime(expiredTime)) #debug
					if expiredTime >= bookTime:
						rule = "//td[@yyrq and @yysd]"
						htmldoc = opener.open(targetUrl, timeout=timeOut).read()
						htmldoc = htmldoc.decode("utf-8", "ignore")
						htmlString = lxml.html.fromstring(htmldoc)
						Datelist = htmlString.xpath(rule)
						tableStr = 'list:\r\n'
						if	Datelist:
							for item in Datelist:
								tableStr += "Date:%s Time:%s Times:%s" %(item.attrib['yyrq'], item.attrib['yysd'], item.text_content().strip())+"\r\n"
						runLog = "date: %s %s times:%s not found the button" % (searchDate, searchTime, leftTime)
						runLog += tableStr
						errorLog(runLog)
					else:
						runLog="%s %s car  must before %s" %(searchDate, searchTime, time.strftime("%Y-%m-%d", time.localtime(expiredTime)))
						errorLog(runLog)

		else:
			runLog = "you did'nt choose a book time"
			errorLog(runLog)
			
	except urllib2.HTTPError, error:
			runLog = error.read()
			errorLog(runLog)
	except:
		import traceback,sys
		runLog="".join(traceback.format_exception(*sys.exc_info()))
		errorLog(runLog)
		print "Oh, we got a problem!"
			
#获取预约时间当天所有车辆
def getCars(wDate, wTime):
	waitTime()
	global wcookie, opener, carList
	targetUrl = 'http://haijia.bjxueche.net/Han/ServiceBooking.asmx/GetCars'
	postData = {
		'pageNum':1,
		'pageSize':35,
		'xllxID':'2',
		'yyrq':str(wDate),
		'yysd':str(wTime),
	}
	#记录日志
	runLog = "get Cars..."
	errorLog(runLog)
	req = urllib2.Request(targetUrl, json.dumps(postData), {'Content-Type': 'application/json'})
	try:
		jsondoc = opener.open(req, timeout=timeOut).read().replace('_1','')
		#去掉无用字符
		jsondoc = re.sub(ur"(_\d?)", '', jsondoc)
		jsontext = json.loads(jsondoc)
		jsonData = json.loads(jsontext['d'])

		for items in jsonData:
			for (k,v) in items.items():
				if k == "CNBH":
				 	carList.append(v)
		#开始约车
		bookingCar(wDate, wTime)
	except:
		import traceback,sys
		runLog="".join(traceback.format_exception(*sys.exc_info()))
		errorLog(runLog)
		print "Oh, we got a problem!"

#预约车
def bookingCar(wDate, wTime):
	waitTime()
	targetUrl = 'http://haijia.bjxueche.net/Han/ServiceBooking.asmx/BookingCar'
	postData = {
		'KMID':'2',
		'cnbh':carList[0],
		'imgCode':md5.md5(postCookie['txtBookingCode'].upper()).hexdigest(),
		'yyrq':str(wDate),
		'xnsd':str(wTime),
	}
	runLog = "Booking Car"
	errorLog(runLog)
	myHeader = {
		'Content-Type': 'application/json',
		'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
		'Referer':'http://haijia.bjxueche.net',
	}
	req = urllib2.Request(targetUrl, json.dumps(postData), myHeader)
	try:
		jsondoc = opener.open(req, timeout=timeOut).read()
		jsontext = json.loads(jsondoc)
		jsonData = json.loads(jsontext['d'])
		if jsonData[0]['Result'] == True:
			writeLock(wDate, wTime)
			runLog = "Booking car done!"
			errorLog(runLog)
		runLog = jsondoc
		errorLog(runLog)
	except urllib2.HTTPError, error:
	 	runLog = error.read()
		errorLog(runLog)
	except:
		import traceback,sys
		runLog="".join(traceback.format_exception(*sys.exc_info()))
		errorLog(runLog)
		print "Oh, we got a problem!"

def errorLog(log):
	logHeader = "*******************\r\n"
	logFooter = "*******************\r\n"
	if outPut == 1:
		logHeader += time.strftime("%Y-%m-%d %X", time.localtime())+"\r\n"
		print logHeader
		print log
		print logFooter
	else:
		f = file(logPath+user+'.log', "aw")	
		logHeader += time.strftime("%Y-%m-%d %X", time.localtime())+"\r\n"
		logHeader += "username: %s" %(username)+"\r\n"
		f.write(logHeader)
		f.write(log+"\r\n")
		f.write(logFooter)
		f.close()

def writeLock(wDate, wTime):
	lockDir = {}
	#文件存在则读取文件,不存在则创建新的
	if os.path.exists(logPath+user+'.lock'):
		f = file(logPath+user+'.lock', 'r')
		lockDir = cPickle.load(f)
		f.close()
	else:		
		for item in users[user]['date']:
			configDate = todayYear+item[0]
			configTime = reserveTimeData[item[1]]
			lockDir[configDate+'_'+configTime] = '0'	
	#容错，如果文件存在且内容不正确 则重新写入文件内容
	if 	not lockDir:
		for item in users[user]['date']:
			configDate = todayYear+item[0]
			configTime = reserveTimeData[item[1]]
			lockDir[configDate+'_'+configTime] = '0'	

	lockDir[wDate+'_'+wTime] = '1'	
	f = file(logPath+user+'.lock', 'w')
	cPickle.dump(lockDir, f)
	f.close()

def checkLock():
	lockDir = {}
	if os.path.isfile(logPath+user+'.lock'):
		f = file(logPath+user+'.lock', 'r')
		lockDir = cPickle.load(f)
		f.close()
		if lockDir:
			#检测到所有日期的车都约过了的时候就会返回真，让脚本停止
			for item in users[user]['date']:
				configDate = todayYear+item[0]
				configTime = reserveTimeData[item[1]]
				bookTime =  time.mktime(time.strptime(configDate,'%Y%m%d'))
				expiredTime =  int(time.time())+3600*24*7
				#print time.strftime("%Y-%m-%d ", time.localtime(expiredTime)) #debug
				if expiredTime >= bookTime:
					if not lockDir.has_key(configDate+'_'+configTime) or lockDir[configDate+'_'+configTime] == '0':
						return False
					else:
						runLog="%s %s car is already booked!" %(item[0], item[1])
						errorLog(runLog)
				else:
					runLog="%s %s car  must before %s" %(item[0], item[1], time.strftime("%Y-%m-%d", time.localtime(expiredTime)))
					errorLog(runLog)
				
			return True
		else:
			return False
	else:
		return False
#随机等待时间，不然IP会被封，如果被封，24小时以后解禁。也可以打电话给客服。
def waitTime():
	sec = random.randint(1, 6)
	runLog="wait %s seconds because not will be forden the IP!" %(sec)
	errorLog(runLog)
	time.sleep(sec)

if checkLock():	
	runLog="%s 'job done!" %(username)
	errorLog(runLog)
	exit(0)
	
waitTime()
hjLogin(username,password,targetUrl)

