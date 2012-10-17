#!/usr/bin/python
import sys ,os, stat
################################################
class ShortInputException(Exception):
	'''input filename'''
	def __init__(self, length, atleast):
		Exception.__init__(self)
		self.length = length
		self.atleast = atleast
try:
	if sys.argv[1] is None:
		s = raw_input('Enter somefile of python --> ')
	else:
		s= sys.argv[1]
	if len(s) < 1:
		raise ShortInputException(len(s), 1)
except EOFError:
	print '\nSorry! u stop it by ctrl+D'
	sys.exit()
except ShortInputException, x:
	print 'ShortInputException: The input was of length %d, \
          was expecting at least %d' % (x.length, x.atleast)
	sys.exit()
else:
	print 'input is Done! param:%s' % s
################################################
if	s.find('.py') == -1:
	filename = s+'.py'
else:
	filename = s

if	os.path.isfile(filename):
	print "%s is exist!" % filename
	exit
	
content = '''\
#!/usr/bin/python
#Filename : %s
#Author   :   Will
''' % filename

if	filename:
	f = file(filename, 'w')
	f.write(content)
	f.close()
	os.chmod('./'+filename, stat.S_IRWXU)
	print 'Done!'
