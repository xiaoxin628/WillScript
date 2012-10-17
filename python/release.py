#!/usr/bin/python
#coding:utf-8
#Filename : release.py
#Author   :   Will
from Tkinter import *
import os, sys ,stat, re, gzip, pexpect, tkFont
#config
username = 'lishuzu@gmail.com'
password = 'tp5yW7fp8KT3'
svnHome = '/home/wwwroot/testapp/svnhome'
sourceDir = 'https://coldxin.googlecode.com/svn/trunk/php/ColdXin_CI'
serverDir = '/home/wwwroot/test/'
serverIp = '10.237.39.91'
serverUsr = 'test'
serverPwd = 'xiaomi123'
svnBin = '/usr/bin/svn'
oldARG = 4
newARG = 0
GUI = 1

#GUI
class App:
	frame = ''
	master = ''
	def __init__(self, master):
		self.master = master
		self.layout()
		self.frame = Frame(self.master)
		self.frame.pack()
		self.component()
	def layout(self):
		#master
		self.master.resizable(False, False)
		self.master.title('release 1.0')
		self.master.update()
		scnWidth, scnHeight = self.master.maxsize()
		curWidth = 800
		curHeight = scnHeight*0.7
		screenCnf = '%dx%d+%d+%d'%(curWidth,curHeight,((scnWidth-curWidth)/2)*0.1,(scnHeight-curHeight)/2)
		self.master.geometry(screenCnf)

		# Component
	def component(self):
		textFont = tkFont.Font(weight="bold")
		self.logText = Text(self.frame, background='black', foreground="green", highlightcolor="green", font=textFont, width=100, height=18)
		print dir(self.logText)
		self.logText.pack(expand=yes)

		self.releaseButton = Button(self.frame, text="Release", command = self.release)
		self.releaseButton.pack(side=LEFT)

		self.button = Button(self.frame, text="QUIT", fg="red", command=self.frame.quit)
		self.button.pack(side=RIGHT)

	def release(self):
		release()

	def logOut(self, log):
		self.logText.insert('end', log)
		self.logText.insert('end', "\n")
		self.master.update()

#lib
def getInfo():
	'''geti the svn info'''
	info = [];
	for line in os.popen('svn info ' + sourceDir):
		info.append(line)
	return info

def release():
	if not os.path.exists(svnHome):
		try:
			logstr = "mkdir"+svnHome
			log(logstr)

			os.makedirs(svnHome)
			# os.chmod(svnHome, stat.S_IRWXU)
			os.makedirs(svnHome+'/data/code')
			os.makedirs(svnHome+'/data/log')
			os.makedirs(svnHome+'/data/upload')
		except Excesplitption:
			logstr = "mkdir is fail!"
			log(logstr)
			pass
	#define the dir of the project
	project = os.path.split(sourceDir)[1]
	command = '%s co %s %s --force --username %s --password %s' % (svnBin, sourceDir, svnHome+'/data/code/'+project, username, password)
	os.system(command)
	logstr = '%s co %s %s --force --username %s' % (svnBin, sourceDir, svnHome+'/data/code/'+project, username)
	log(logstr)

	#delete the file
	os.system('rm -rf '+svnHome+'/data/upload/'+project+'/*')
	#svn lastVersion 
	lastVersion = re.search(ur"(\d)+", str(getInfo()[4]).decode('utf8'))
	if lastVersion:
		newARG = int(lastVersion.group(0))
	log('lastVersion is {lastV} !'.format(lastV = newARG))

	if newARG:
		if not oldARG:
			command = '%s diff -c %d --summarize %s --summarize' % (svnBin, newARG ,sourceDir)
		else:
			command = '%s diff -r %d:%d --summarize %s --summarize' % (svnBin, oldARG, newARG ,sourceDir)

		log(command)
		for line in os.popen(command):
				linelist = line.split(' ')
				fileName = str(linelist[7].strip())
				if fileName:
			 		filePath = os.path.split(fileName.replace(sourceDir, ''))[0]
				 	fullName = fileName.replace(sourceDir, '')
				 	exportSrcFile = svnHome+'/data/code/'+project+fullName
				 	exportDesFile = svnHome+'/data/upload/'+project+fullName
					if not filePath.endswith('/'):
						filePath = filePath+'/'
					try:
						exportDesPath= svnHome+'/data/upload/'+project+filePath
						if not os.path.exists(exportDesPath):
							os.makedirs(exportDesPath)
					except OSError:
						log(exportDesPath+' mkdir fail! exists!')
						pass
					# command = '%s export -r %d %s %s --force --username %s --password %s' % (svnBin, newARG, exportSrcFile, exportDesFile, username, password)
					command = 'cp -r %s %s' %(exportSrcFile, exportDesFile) 
					os.system(command)
					log(exportDesFile)
	command = 'rsync -avz %s %s@%s:%s' % (svnHome+'/data/upload/'+project, serverUsr, serverIp, serverDir)
	shell = pexpect.spawn(command)
	i = shell.expect(['password:', 'continue connecting (yes/no)]?'])
	if i == 0:
		shell.sendline(serverPwd)
	elif i ==1:
			shell.sendline('yes\n')
			shell.expect('password:')
			shell.sendline(serverPwd)
	shell.read()
	log(command)

 # log formate
def log(log):
	global app 
	if GUI:
		app.logOut(log+"\n")
	else:
		print log

if GUI:
	root = Tk()
	app = App(root)
	root.mainloop()
else:
	release()