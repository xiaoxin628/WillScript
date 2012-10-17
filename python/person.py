#!/usr/bin/python
#Filename : testobj.py
#coding:utf-8
#Author   :   Will
_metaclass__ = type
class Person:
	def setName(self, name):
		self.name = name
	def getName(self, name):
		return self.name
	def greef(self):
		print "Hello,world! I'm %s" % self.name
def say():
	print "this is anthor methond"
foo = Person()
foo.setName('Look')
foo.greef()
foo.greef = say
foo.greef()
#foo = Person()
#bar = Person()
#foo.setName('Look')
#bar.setName('Anakin')
#foo.greef()
#bar.greef()
