#!/usr/bin/python
# -*- coding: UTF-8 -*-
import wx
import cv

#from cv.highgui import *
 
class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'camera')
        self.SetClientSize((640, 480))
 
        self.cap = cvCreateCameraCapture(0)
        self.Bind(wx.EVT_IDLE, self.onIdle)
 
    def onIdle(self, event):
        img = cvQueryFrame(self.cap)
        self.displayImage(img)
        event.RequestMore()
 
    def displayImage(self, img, offset=(0,0)):
        bitmap = wx.BitmapFromBuffer(img.width, img.height, img.imageData)
        dc = wx.ClientDC(self)
        dc.DrawBitmap(bitmap, offset[0], offset[1], False)
 
if __name__=="__main__":
    app = wx.App()
    frame = MyFrame()
    frame.Show(True)
    app.MainLoop()