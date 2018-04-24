#!/usr/bin/python
print '...'
import os
import sys

home_url = "/home/huyheo/work/Project/HD1002"

try:
	target_file = sys.argv[1]
	target2 = sys.argv[2]
except:
	print 'no input parameter.'




#########################
# clean checkout
# make world
##########################*/
def clean_build():
    print "### cd "+ home_url  
    if (os.path.isdir(home_url)):
        print 'Folder is existed.'
        os.system("sudo rm -fr " + home_url)
    
    os.system("mkdir " + home_url)

    print "move to " + home_url
    os.chdir(home_url)

    print "svn co http://svn.humaxdigital.com/drr_cdi/trunk/models/hdr-1002s_ph3/ ./hdr-1002s-ph3"
    os.system("svn co http://svn.humaxdigital.com/drr_cdi/trunk/models/hdr-1002s_ph3/ ./hdr-1002s-ph3")
   
    new_home_url = os.path.join(home_url,"hdr-1002s-ph3")

    print "### cd model/down"
    os.chdir(new_home_url + "/model/down")

    print "### ./down.sh full_head"
    os.system("./down.sh full_head")

    print "### make hdr-1002s-ph3_hwtest_defconfig"
    os.chdir(new_home_url +"/make")
    os.system("make hdr-1002s-ph3_hwtest_defconfig")


    print "### make world"
    os.system("make world")

    print "### make image-initrd"
    os.system("make image-initrd")

    print "### Create Revision Info file" 
    os.chdir(new_home_url + "/model/down")
    os.system("./down.sh full_head local_info > full_release_RXXXX")



"""
if sys.argv[1] == 'clean':
    clean_build(sys.argv[2])
if sys.argv[2]:
    clean_build(sys.argv[2])
elif target_file == 'help':
    print 'help'
"""
if 1:
    clean_build()
    
