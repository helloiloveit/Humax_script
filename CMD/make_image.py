#!/usr/bin/python
print '...'
import os
import sys

home_url = "/home/huyheo/work/Project/Test_New_Co"

try:
	target_file = sys.argv[1]
except:
	print 'wrong input, pls try again'
	exit()
print "### cd "+ home_url  
os.system("rm -fr " + home_url)
os.system("mkdir " + home_url)
os.chdir(home_url)
print "svn co http://svn.humaxdigital.com/drr_cdi/trunk/models/t51/ ./"
os.system("svn co http://svn.humaxdigital.com/drr_cdi/trunk/models/t51/ ./")

print "### cd model/down"
os.chdir(home_url + "/model/down")
os.chdir("/home/huyheo/work/Project/Test_New_Co/model/down")
os.system("ls -l")
print "### ./down.sh full_head"
os.system("./down.sh full_head")

print "### make t51_rev01_epg_defconfig"
os.chdir(home_url +"/make")
os.system("make t51_rev01_epg_defconfig")

print "### make world"
os.system("make world")

#optional for typing password
os.system("maiphuong")
os.system("maiphuong")


print "### make image-mrs"
os.system("make image-mrs")
