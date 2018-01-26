#!/usr/bin/python
print '...'
import os
import sys

home_url = "/home/huyheo/work/Project/"
epg_url = "/home/huyheo/work/Project/Test_New_Co/model/epg/NDS"
#tftp_url = "/home/huyheo/work/tftpboot/t52"
tftp_url = "/home/huyheo/work/tftpboot/"
final_binary=" "

try:
	mode  = sys.argv[1]
except:
	print 'Need info of Type: debug or release'
	exit()

try:
	target_file = sys.argv[2]
except:
	print 'No Binary name.  Ex: T51_73535_CDI_24Feb2017_R11052.tar.bz2'
	exit()


def validate_env():
    os.chdir(home_url)
    print "### cd "+ home_url

    if (os.path.isdir("release_buildtree")):
        print "Extracted build tree is existed. Delete it..."
        os.system("sudo rm -fr " + "release_buildtree")
    else:
        print "No dir is existed.Go .."

def copy_EPG_from_svn(mode):
    os.chdir(home_url + "release_buildtree/bin/uclinux-rootfs/debug/skel")
    print "### Copy EPG from "+ epg_url 
    print "cp -fr " + epg_url + " ."
    os.system("cp -fr " + epg_url + " .")

def copy_image_to_tftp(mode):
    print "### Copy to Tftp folder"
    print "cp " + os.path.join(home_url,"release_buildtree/misc/buildsys/../../bin/squashfs/",mode,final_binary) +" " + tftp_url
    os.system("cp " + os.path.join(home_url,"release_buildtree/misc/buildsys/../../bin/squashfs/",mode,final_binary) +" " + tftp_url)

########################
# Get prj name
########################
def get_prj_name():
    print "Getting prj name... :" + sys.argv[2] 
    prj_name = sys.argv[2].split("_")[0]
    if prj_name == "HDR":
        print "HDR prj"
	global final_binary
	final_binary = "vmlinuz-squashfs-7346b0_mrs.bin"
        return "hdr-1002s-ph3"
    elif prj_name == "T51":
        print "T51 prj"
	global final_binary 
	final_binary = "vmlinuz-squashfs-73465a0_mrs.bin"
	return "t51"
    elif prj_name =="T52":
        print "T52 prj"
	global final_binary
	final_binary = "vmlinuz-squashfs-73465a0_mrs.bin"
	return "t52"
    else:
        print prj_name + " is not defined. Try again"
	raise Exception(" Prj is not defined")



########################
# Create release binary
########################
def create_release():

    print "To build Image from Release Binary :" + target_file
    validate_env()

    print "sudo tar -xjvf " + target_file
    os.system("sudo tar -xjvf " + target_file)
    if (os.path.isdir("release_buildtree")):
        print 'Directory is unpacked successfully'
    else:
        print 'ERROR, check the image again'


    print "### Build Image"
    print "change to Dir: " + home_url + "release_buildtree/misc/buildsys"
    os.chdir(home_url + "release_buildtree/misc/buildsys")

    print "Build:"
    if mode =='release_print':
        os.system("./humax_gen_squashfs_for_release_tree.sh release_print")
    elif mode =='release':
        os.system("./humax_gen_squashfs_for_release_tree.sh release")

    if(os.path.exists(os.path.join(home_url, "release_buildtree/misc/buildsys/../../bin/squashfs/debug/",final_binary))):
        print final_binary + " is generated succsssfully."

    copy_image_to_tftp(mode)

    print "Done"
########################
# Create debug  binary
########################
def create_debug():
    print "To build Image from Release Binary :" + target_file
    validate_env()

    print "sudo tar -xjvf " + target_file
    os.system("sudo tar -xjvf " + target_file)
    if (os.path.isdir("release_buildtree")):
        print 'Directory is unpacked successfully'
    else:
        print 'ERROR, check the image again'

    copy_EPG_from_svn(mode)

    print "### Build Image"
    print "change to Dir: " + home_url + "release_buildtree/misc/buildsys"
    os.chdir(home_url + "release_buildtree/misc/buildsys")

    print "Build:"
    os.system("./humax_gen_squashfs_for_release_tree.sh debug")
    if(os.path.exists(os.path.join(home_url, "release_buildtree/misc/buildsys/../../bin/squashfs/debug/",final_binary))):
        print final_binary + " is generated succsssfully."

    copy_image_to_tftp(mode)

    print "Done"

try:
	prj_name = get_prj_name()
	tftp_url = os.path.join(tftp_url, prj_name)
	print "tftp url = " + tftp_url
	print "final_binary = " + final_binary
 
 
except:
	print "Could not get Prj Name"
	exit()

if mode == 'debug':
    create_debug()
elif mode == 'release':
    create_release()
elif mode == 'release_print':
    create_release()
    
