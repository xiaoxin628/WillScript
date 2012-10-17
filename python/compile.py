#!/usr/bin/python
#Filename : compile.py
#Author   :   Will
import sys, py_compile, os, stat
try:
	s = sys.argv[1]
except:
	print "params is wrong"

if s.find('pyc') != -1:
	print s+' is the pyc.'
	sys.exit()
py_compile.compile(s)
os.chmod(s, stat.S_IRWXU)
