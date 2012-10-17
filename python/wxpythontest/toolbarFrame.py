#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#Filename : toolbarFrame.py
#Author   :   Will
#Email   :   lishuzu@gmail.com
import wx
import wx.py.images as images
class ToolbarFrame(wx.Frame):
	"""docstring for ToolbarFrame"""
	def __init__(self, parent,id):
		wx.Frame.__init__(self, parent, id, 'Toolbars', size=(300,200))
		panel = wx.Panel(self)
		panel.SetBackgroundColour('White')
		statusBar = self.CreateStatusBar()
		toolbar = self.CreateToolBar()
		toolbar.AddSimpleTool(wx.NewId(), images.getPyBitmap(),'New',"Long help for 'New'")
		toolbar.Realize()
		menuBar = wx.MenuBar()
		menu1 = wx.Menu()
		menuBar.Append(menu1, '&File')
		menu1.AppendSeparator() 
		menu2 = wx.Menu()
		menu2.Append(wx.NewId(), "&Copy", 'Copy in status bar')  
		menu2.Append(wx.NewId(), 'C&ut', '')   
		menu2.Append(wx.NewId(), 'Paste', '')                     
		menu2.AppendSeparator()                                   
		menu2.Append(wx.NewId(), '&Options...', 'Display Options')
		menuBar.Append(menu2, '&Edit') # 在菜单栏上附上菜单
		self.SetMenuBar(menuBar)  # 在框架上附上菜单栏
if __name__ == '__main__': 
    app = wx.PySimpleApp() 
    frame = ToolbarFrame(parent=None, id=-1)
    frame.Show()
    dlg = wx.MessageDialog(None, 'Is this the coolest thing ever!','MessageDialog', wx.YES_NO | wx.ICON_QUESTION)
    result = dlg.ShowModal()
    dlg.Destroy()
    app.MainLoop()

