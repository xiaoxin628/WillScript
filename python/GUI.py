#!/usr/bin/python
#coding:utf-8
#Filename : GUI.py
#Author   :   Will
from Tkinter import *
class App:
	"""GUI test"""
	frame = ''
	def __init__(self, master):
		self.layout(master)
		self.frame = Frame(master)
		self.frame.pack()
		self.screenOut()

	def layout(self,master):
		master.resizable(False,False)
		master.title('代码发布1.0')
		master.update()
		curWidth = 800
		curHeight = 600 
		scnWidth,scnHeight = master.maxsize()
		screenCnf = '%dx%d+%d+%d'%(curWidth,curHeight,(scnWidth-curWidth)/2,(scnHeight-curHeight)/2)
		master.geometry(screenCnf)

	def screenOut(self):
		self.logOut = Text(self.frame)
		self.logOut.tag_config('b', foreground='blue')

		self.button = Button(self.frame, text="QUIT", fg="red", command=self.frame.quit)
		self.button.pack(side=LEFT)

		self.hi_there = Button(self.frame, text="Hello", command=say_bye(self))
		self.hi_there.pack(side=LEFT)


		for i in range(10):
		    self.logOut.insert(1.0,'0123456789 ')
		self.logOut.pack()


	def say_hi(self):
		self.logOut.insert(1.0,'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
		# say_bye(self)

def say_bye(obj):
	obj.logOut.insert(1.0,'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')

root = Tk()
app = App(root)
app.say_hi()
root.mainloop()