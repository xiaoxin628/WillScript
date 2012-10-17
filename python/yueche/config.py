#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#Filename : config.py
#Author   :   Will
#Email   :   lishuzu@gmail.com

#超时时间 s
timeOut = 120
#是否输出到屏幕 1为输出 0则输出到当前目录下的日志中
outPut = 1

version = "1.2"

users = {}
#账户信息 多人请赋值多份
users['will'] = {}
users['will']['username'] = ''
users['will']['password'] = ''
users['will']['date'] = []
users['will']['date'].append(['1121', 'morning'])
users['will']['date'].append(['1023', 'night'])
users['will']['date'].append(['1022', 'night'])

