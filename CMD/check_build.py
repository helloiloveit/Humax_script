#!/usr/bin/python
print '...'
import os
import sys

home_url = "/home/huyheo/work/Project/Test_New_Co"

try:
	target_file = sys.argv[1]
	target2 = sys.argv[2]
except:
	print 'wrong input, pls try again'
	exit()

print 'target_file', sys.argv[1], sys.argv[2]
os.system("sudo -S <<< 'maiphuong' ls -l")



#########################
# clean checkout
# make world
##########################*/
def clean_build(version):
    print "### cd "+ home_url  
    if (os.path.isdir(home_url)):
        print 'Folder is existed.'
        os.system("rm -fr " + home_url)
    
    os.system("mkdir " + home_url)

    print "move to " + home_url
    os.chdir(home_url)

    print "svn co http://svn.humaxdigital.com/drr_cdi/trunk/models/t51/ ./"
    os.system("svn co http://svn.humaxdigital.com/drr_cdi/trunk/models/t51/ ./")

    print "### cd model/down"
    os.chdir(home_url + "/model/down")

    if version == '256':
        print "### ./down.sh full_release_256MB"
        os.system("./down.sh full_release_256MB")

        print "### make t51_rev01_epg_defconfig"
        os.chdir(home_url +"/make")
        os.system("make t51_rev01_epg_defconfig")
    else: #512MB
        print "### ./down.sh full_head"
        os.system("./down.sh full_head")

        print "### make t51_rev03_epg_defconfig"
        os.chdir(home_url +"/make")
        os.system("make t51_rev03_epg_defconfig")

    print "### make world"
    os.system("make world")

    print "### make image-mrs"
    os.system("make image-mrs")

    print "### Create Revision Info file" 
    os.chdir(home_url + "/model/down")
    os.system("./down.sh full_head local_info > full_release_RXXXX")




if sys.argv[1] == 'clean':
    print 'clean checkout, build all'
if sys.argv[2]:
    clean_build(sys.argv[2])
elif target_file == 'help':
    print 'help'
