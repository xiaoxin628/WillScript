#!/usr/bin/python
#coding:utf-8
#Filename : hackyueche.py
#Author   :   Will

import lxml.html, lxml.etree
import sys, os, urllib, urllib2, cookielib, Cookie, datetime, time, json, md5, re, cPickle, random ,pprint
from config import *
reload(sys)
sys.setdefaultencoding("utf-8")

#lib
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
			runLog = "error:" , contents
			errorLog(runLog)
			exit()
	except  urllib2.URLError, error:
			runLog = "error:",  error.reason
			errorLog(runLog)
			exit()
	except:
		import traceback,sys
		runLog="".join(traceback.format_exception(*sys.exc_info()))
		errorLog(runLog)
		print "Oh, we got a problem!"
		exit()

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
						if bookTime < int(time.time()):
							runLog="your date: %s %s is passed. remove it from config" %(searchDate, searchTime)
							errorLog(runLog)
						else:
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
						runLog="only book car before %s !your date: %s %s" %(time.strftime("%Y-%m-%d", time.localtime(expiredTime)), searchDate, searchTime)
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
			#写入成功锁文件
			writeLock(wDate, wTime)
			runLog = "Booking car done!"
			errorLog(runLog)
			#发送邮件
			wMessage = "用户%s 在%s %s 已经预约成功，请登录http://haijia.bjxueche.net查看" %(username, wDate, wTime)
			if wEmail:
				sendEmail("yueche@yueche.com", wEmail, "约车结果", wMessage)
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
					runLog="only book car before %s !your date: %s %s" %(time.strftime("%Y-%m-%d", time.localtime(expiredTime)), item[0], item[1])
					errorLog(runLog)
				
			return True
		else:
			return False
	else:
		return False
#随机等待时间，不然IP会被封，如果被封，24小时以后解禁。也可以打电话给客服。
def waitTime():
	sec = random.randint(1, 5)
	runLog="wait %s seconds or not the IP will be banned!" %(sec)
	errorLog(runLog)
	time.sleep(sec)
#mail someone
def sendEmail(wFrom, wTo, wTitle, wMessage):
	SENDMAIL = "/usr/sbin/sendmail" # sendmail location
	p = os.popen("%s -fName -t" % SENDMAIL, "w")
	p.write("From: "+wFrom+"\n")
	p.write("To: "+wTo+"\n")
	p.write("Subject: "+wTitle+"\n")
	p.write("\n") # blank line separating headers from body
	p.write(wMessage+"\n")
	sts = p.close()
	if sts is not None:
		runLog = "Sendmail exit status"+str(sts)
		errorLog(runLog)




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
wEmail = users[user]['email']
reserveDate = ""
reserveTime = ""
logPath = sys.path[0]+"/"

#默认代理
if enable_proxy:
	wProxy = random.choice(proxyList)
else:
	wProxy = 'default'


#定义验证码 每次都用同一个验证码
postCookie = {
	'txtIMGCode':codeList[wProxy]['txtIMGCode'],
	'ImgCode':codeList[wProxy]['ImgCode'],
	'txtBookingCode':codeList[wProxy]['txtBookingCode'],
	'BookingCode':codeList[wProxy]['BookingCode'],
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
#设置登录验证码cookie
wcookie.set_cookie(cookielib.Cookie(version=0, name='ImgCode', value=postCookie['ImgCode'], port=None, port_specified=False, domain='haijia.bjxueche.net', domain_specified=False, domain_initial_dot=False, path='/', path_specified=True, secure=None, expires=(int(time.time())+3600*24*30), discard=False, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False))

#设置约车验证码cookie
wcookie.set_cookie(cookielib.Cookie(version=0, name='BookingCode', value=postCookie['BookingCode'], port=None, port_specified=False, domain='haijia.bjxueche.net', domain_specified=False, domain_initial_dot=False, path='/', path_specified=True, secure=None, expires=(int(time.time())+3600*24*30), discard=False, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False))
siteCookie = urllib2.HTTPCookieProcessor(wcookie)
#增加代理
if enable_proxy:
	wProxy_handler = urllib2.ProxyHandler({'http': 'http://'+wProxy+'/'})
	runLog = 'proxy:'+wProxy+'\r\n'
	errorLog(runLog)
else:
	wProxy_handler = urllib2.ProxyHandler({})
	
opener = urllib2.build_opener(siteCookie, wProxy_handler)	

opener.addheaders = [
        ('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:14.0) Gecko/20100101 Firefox/14.0.1 '),
        ('Referer','http://haijia.bjxueche.net'),
        ('Content-Type','text/html'),
        ('Accept-Charset','UTF-8'),
]

urllib2.install_opener(opener)

#测试代理服务器
#req = urllib2.Request('http://ip.chinaz.com/')
#htmldoc = opener.open(req, timeout=timeOut).read()
#print htmldoc
#exit()
	

if checkLock():	
	runLog="%s 'job done!" %(username)
	errorLog(runLog)
	exit(0)
	
waitTime()
hjLogin(username,password,targetUrl)
exit()

