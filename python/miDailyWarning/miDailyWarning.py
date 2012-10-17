#!/usr/bin/python
#coding:utf-8
#Filename : miDailyWarning.py
#Author   :   Will
#mail	  :   lishuzu@xiaomi.com
#crontab -e
#DISPLAY=:0.0
#30 20 * * 1-6 /home/will/Dropbox/willcode/Script/miDailyWarning/miDailyWarning.py

import os, tkFont
from Tkinter import *
from config import *

class App:
	"""just remind u to write the daily report! """
	frame = ''
	master = ''
	def __init__(self, master):
		self.master = master
		self.layout()
		self.frame = Frame(self.master)
		self.frame.pack()
		self.screenOut()

	def layout(self):
		self.master.resizable(False,False)
		self.master.title('hi 日报时间到了')
		self.master.update()
		scnWidth,scnHeight = self.master.maxsize()
		curWidth = scnWidth-200
		curHeight = scnHeight-200
		screenCnf = '%dx%d+%d+%d'%(curWidth,curHeight,(scnWidth-curWidth)/2,(scnHeight-curHeight)/2)
		self.master.geometry(screenCnf)

	def screenOut(self):
		textFont = tkFont.Font(size="60", weight="bold")
		self.remindText = Label(self.frame, text='温馨提示:该写日报了!', fg="red", width=self.master.winfo_reqwidth(), height="1", font=textFont)
		self.remindText.pack(side="top")
		photo = PhotoImage(file = codeDir+'dailyphoto.gif')
		self.remindImage = Button(self.frame, compound='top' ,image=photo, width="500", height="500", command=self.openFile)
		self.photo = photo
		self.remindImage.pack(side="top", fill="both", expand="yes")
		self.button = Button(self.frame, text="暂时不写", fg="red", command=self.frame.quit)
		self.button.pack(side="bottom")
		if localDoc:
			self.button = Button(self.frame, text="同步", fg="blue", command=self.copyDaily)
			self.button.pack(side="bottom")

	def openFile(self):
		if localDoc:
			command = 'echo '+rootPwd+'| sudo -S gnome-open \''+unicode(localDoc,"utf-8").encode('utf-8')+'\''
		else:
			command = 'echo '+rootPwd+'| sudo -S gnome-open \''+unicode(dailyDoc,"utf-8").encode('utf-8')+'\''
		os.system(command)

	def copyDaily(self):
		command = "echo "+rootPwd+"|sudo -S cp "+localDoc+" "+dailyDoc
		os.system(command)
		Label(self.frame,text = '同步完成',width = 60,fg="red").pack(side="bottom")

if not os.path.isfile(dailyDoc):
	command = 'echo '+rootPwd+'|sudo -S mount //10.237.2.61/sharefiles/ '+mountDir+' -o "iocharset=utf8,username='+mailUsername+',password='+mailPassword+',dmask=777,fmask=777,codepage=cp936,uid=0"'
	os.system(command)
root = Tk()
app = App(root)
root.mainloop()