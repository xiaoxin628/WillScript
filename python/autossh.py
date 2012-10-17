#!/usr/bin/python
#coding:utf-8
#Filename : autossh.py
#Author   :   Will
import pexpect
command = 'ssh test@10.237.39.91'
ssh = pexpect.spawn(command)
try:
	ssh.expect('password:')
	ssh.sendline('111')
	print ssh.read()
except pexpect.EOF:
	print 'EOF'
	ssh.close()
except pexpect.TIMEOUT:
	print 'TIMEOUT'
	ssh.close()
