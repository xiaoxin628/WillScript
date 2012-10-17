#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#Filename : teststd.py
#Author   :   Will
#Email   :   lishuzu@gmail.com
import wx
import sys
class Frame(wx.Frame):
	"""teststd"""
	def __init__(self, parent,id,title):
		print "Frame __init__"		
		wx.Frame.__init__(self,parent,id,title)
class App(wx.App):
	"""some"""
	def __init__(self, redirect=True, Filename=None):
		print "App__init__"
		wx.App.__init__(self, redirect, Filename)

	def OnInit(self):
		print "OnInit"
		self.frame = Frame(parent=None, id=-1, title="Startup")
		self.frame.Show()
		self.SetTopWindow(self.frame)
		print >> sys.stderr, "A pretend error message"
		return True				
	def OnExit(self):
		print "OnExit"
if __name__=='__main__':
	app = App(redirect=True)
	print "before MainLoop"
	app.MainLoop()
	print "after MainLoop"
	app.ExitMainLoop()