#!/usr/bin/python
print '...'
import os
import sys

home_url = "/home/huyheo/work/Project/Test_New_Co"

try:
	target1 = sys.argv[1]
except:
	print 'wrong input, pls try again'
	exit()

try:
	target2 = sys.argv[2]
except:
    target2 = ''  

def make_release(target2):
    if target2 =='print':
        print "### make t51_rev03_rel_dbg_defconfig"
        os.chdir(home_url +"/make")
        os.system("make t51_rev03_rel_dbg_defconfig")
    elif target2 =='release':
        print "### make t51_rev03_rel_defconfig"
        os.chdir(home_url +"/make")
        os.system("make t51_rev03_rel_defconfig")
    else:
        print "wrong option"
        exit()
        

    print "### make world"
    os.system("make world")

    #optional for typing password
    os.system("maiphuong")
    os.system("maiphuong")


    print "### make image-mrs"
    os.system("make image-mrs")

def make_debug():
    print "### make t51_rev03_epg_defconfig"
    os.chdir(home_url +"/make")
    os.system("make t51_rev03_epg_defconfig")

    print "### make world"
    os.system("make world")

    #optional for typing password
    os.system("maiphuong")
    os.system("maiphuong")


    print "### make image-mrs"
    os.system("make image-mrs")

if target1 == 'debug':
    make_debug()
elif target1 == 'release':
    make_release(target2)

