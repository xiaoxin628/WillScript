#!/usr/bin/python
#coding:utf-8
#Filename : setup.py
#Author   :   Will
#sudo ./setup.py will /home/will/Dropbox/willcode/Script/python/miDailyWarning/miDailyWarning.py
import os,sys
try:
	user =  sys.argv[1]
	scriptDir =  sys.argv[2]
except Exception:
	print '''
	sudo ./setup.py user [path]/miDailyWarning.py
	
	ex: sudo ./setup.py will /home/will/Dropbox/willcode/Script/miDailyWarning/miDailyWarning.pyc

	'''
	exit()
command = 'apt-get install python-setuptools python-tk'
os.system(command)
print command
command = "echo 'DISPLAY=:0.0' >> /var/spool/cron/crontabs/"+user
os.system(command)
print command
command = "echo '30 20 * * 1-6 /usr/bin/python "+scriptDir+"' >> /var/spool/cron/crontabs/"+user
os.system(command)
print command
print 'Note your crontab will like this:'
command = 'crontab -u '+user+' -l'
print command
os.system(command)
command = 'service cron restart'
os.system(command)
