#!/usr/bin/python
print '...'
import os
import sys


try:
	target_file = sys.argv[1]
except:
	print 'wrong input, pls try again'
	exit()
print 'grep -R --exclude-dir={.svn,.tags} ' + target_file
os.system(" grep -R --exclude-dir={.svn,.tags}  "+ target_file )
