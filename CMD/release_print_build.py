#!/usr/bin/python
print '...'
import os
import sys

home_url = "/home/huyheo/work/Project/"
epg_url = "/home/huyheo/work/Project/Test_New_Co/model/epg/NDS"
#epg_url = "/home/huyheo/work/Project/T51/model/epg/NDS"

try:
	target_file = sys.argv[1]
except:
	print 'wrong input, pls try again'
	exit()

print "To build Image from Release Binary :" + target_file
os.chdir(home_url)
print "### cd "+ home_url

if (os.path.isdir("release_buildtree")):
    print "Extracted build tree is existed. Delete it..."
    os.system("sudo rm -fr " + "release_buildtree")
else:
    print "No dir is existed.Go .."

print "sudo tar -xjvf " + target_file
os.system("sudo tar -xjvf " + target_file)
if (os.path.isdir("release_buildtree")):
    print 'Directory is unpacked successfully'
else:
    print 'ERROR, check the image again'


print "### Build Image"
print "change to Dir: " + home_url + "release_buildtree/misc/buildsys"
#os.chdir(home_url + "release_buildtree/misc/buildsys")
os.chdir(os.path.join(home_url,"release_buildtree/misc/buildsys"))

print "Build:"
os.system("./humax_gen_squashfs_for_release_tree.sh release_print")
if(os.path.exists("/home/huyheo/work/Project/release_buildtree/misc/buildsys/../../bin/squashfs/debug/vmlinuz-squashfs-73465a0_mrs.bin")):
    print "vmlinuz-squashfs-73465a0_mrs.bin is generated."

print "### Copy to Tftp folder"
print "cp /home/huyheo/work/Project/release_buildtree/misc/buildsys/../../bin/squashfs/release_print/vmlinuz-squashfs-73465a0_mrs.bin /home/huyheo/work/tftpboot/t51"
os.system("cp /home/huyheo/work/Project/release_buildtree/misc/buildsys/../../bin/squashfs/release_print/vmlinuz-squashfs-73465a0_mrs.bin /home/huyheo/work/tftpboot/t51")

print "Done"