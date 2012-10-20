#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#Filename : config.py
#Author   :   Will
#Email   :   lishuzu@gmail.com

#超时时间 s
timeOut = 120
#是否输出到屏幕 1为输出 0则输出到当前目录下的日志中
outPut = 1

version = "1.3"

users = {}

enable_proxy = True
#这里是http 代理,默认传媒大学代理，与codeList一一对应
proxyList = [
		'218.247.129.2:80',
		'218.247.129.3:80',
		'218.247.129.4:80',
		'218.247.129.6:80',
		'218.247.129.7:80',
]

#因为生成验证码与IP有关，所以每一个IP对应一个验证码，
#登录验证码url:http://haijia.bjxueche.net/tools/CreateCode.ashx?key=ImgCode&random=0.5527176032187311
#需要用firebug来查看该页面图片所带有的cookie 并记录入本配置文件中

#约车验证码url:http://haijia.bjxueche.net/tools/CreateCode.ashx?key=BookingCode&random=0.07021414325538411
#需要用firebug来查看该页面图片所带有的cookie 并记录入本配置文件中

#txtIMGCode      登录验证码
#ImgCode         登录验证码cookie 
#txtBookingCode  约车验证码
#BookingCode     约车验证码cookie

#默认为北京传媒大学代理,不使用default
codeList = {
	'default':{'txtIMGCode':'hukv','ImgCode':'Q73fsrhw+VE=','txtBookingCode':'pj71','BookingCode':'srs1T66YBYl8c+HCL4WZDi1tEhoiyj/YR2YNhGt0fwV6csMjKJ3gyw=='},
	'218.247.129.2:80':{'txtIMGCode':'prht','ImgCode':'zwCGjVcON/w=','txtBookingCode':'aphy','BookingCode':'jCX1UB4sqRjaKNNlhAJnhyxk+9EpFZphgW80l3fQ8SkBETAZa6eb7g=='},
	'218.247.129.3:80':{'txtIMGCode':'ryyy','ImgCode':'xXxI/s/zXO0=','txtBookingCode':'s7wq','BookingCode':'Py5w7qZpCCjyx7I5atpdf8rvXa1drLtJGMw7KfW4koI0IArh2sS44w=='},
	'218.247.129.4:80':{'txtIMGCode':'jr9h','ImgCode':'Hmf6c1JUH+w=','txtBookingCode':'xjw8','BookingCode':'LMPp0Kn1cASa3e22GKXIWG+YPxIuxY8VtleGweDO8SwT8+pMkWyBiA=='},
	'218.247.129.6:80':{'txtIMGCode':'q6b3','ImgCode':'5VixBmCErQ8=','txtBookingCode':'thn8','BookingCode':'OeV+lxckKcevkn1RWVqTdSo0zLRAPb8B3A644W5w9tKrr8aDtrG2dA=='},
	'218.247.129.7:80':{'txtIMGCode':'htmr','ImgCode':'RTQ59EgjQHA=','txtBookingCode':'5m41','BookingCode':'h00pMqzBKdbt7YTmknRiLhBEbb1zOqfKxG0dM/NOY2GhZd8FllnMMQ=='},
}

#账户信息 多人请赋值多份
#./hackyc.py user1
#users['user1']['date'].append(['date', 'time'])
#date:几月几日 年份程序会自己算出 
#time:时间 morning afternoon night

users['user1'] = {}
users['user1']['username'] = 'xxx'
users['user1']['password'] = 'xxx'
users['user1']['email'] = 'some@some.com'
users['user1']['date'] = []
users['user1']['date'].append(['1020', 'afternoon'])
users['user1']['date'].append(['1021', 'afternoon'])
users['user1']['date'].append(['1028', 'afternoon'])

users['user2'] = {}
users['user2']['username'] = 'xxxxxx'
users['user2']['password'] = 'xxxx'
users['user2']['email'] = 'some@some.com'
users['user2']['date'] = []
users['user2']['date'].append(['1020', 'afternoon'])
users['user2']['date'].append(['1021', 'afternoon'])
users['user2']['date'].append(['1028', 'afternoon'])
