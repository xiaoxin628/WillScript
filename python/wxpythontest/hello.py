#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#Filename : hello.py
#Author   :   Will
#Email   :   lishuzu@gmail.com
'''Hello, wxPython!program.'''
import wx
class Frame(wx.Frame):
	"""Frame class that display an image."""
	def __init__(self, image, parent=None, id=-1,pos=wx.DefaultPosition, title="Hello,wxPython!"):
		"""Create a Frame instance and display image."""
		temp = image.ConvertToBitmap()
		size = temp.GetWidth(),temp.GetHeight()
		wx.Frame.__init__(self, parent, id, title, pos, size, style=wx.DEFAULT_FRAME_STYLE ^(wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX | wx.RESIZE_BORDER |wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX))

		self.bmp = wx.StaticBitmap(parent=self,bitmap=temp)
class App(wx.App):
	"""Application class."""
	def OnInit(self):	
		image = wx.Image('wxPython.jpg', wx.BITMAP_TYPE_JPEG)
		self.frame = Frame(image)
		self.frame.Show()
		self.SetTopWindow(self.frame)
		return True
def main():
	app = App()
	app.MainLoop()
if __name__ == '__main__':	
	main()