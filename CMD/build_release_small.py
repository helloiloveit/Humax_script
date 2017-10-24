#!/usr/bin/python
print '...'
import os
import sys

home_url = "/home/huyheo/work/Project/"
epg_url = "/home/huyheo/work/Project/Test_New_Co/model/epg/NDS"

try:
	target_file = sys.argv[1]
except:
	print 'wrong input, pls try again'
	exit()

print "To build Image from Release Binary :" + target_file
os.chdir(home_url)
print "### cd "+ home_url


if (os.path.isdir("release_buildtree")):
    print 'Dir is existed'
else:
    print 'ERROR, check the image again'


def build_debug():
    print''


def build_release():
    print "### Build Image"
    print "change to Dir: " + home_url + "release_buildtree/misc/buildsys"
    os.chdir(home_url + "release_buildtree/misc/buildsys")

    print "Build:"
    os.system("./humax_gen_squashfs_for_release_tree.sh release")

    print "### Copy to Tftp folder"
    print "cp /home/huyheo/work/Project/release_buildtree/misc/buildsys/../../bin/squashfs/release/vmlinuz-squashfs-73465a0_mrs.bin /home/huyheo/work/tftpboot/t51/"
    os.system("cp /home/huyheo/work/Project/release_buildtree/misc/buildsys/../../bin/squashfs/release/vmlinuz-squashfs-73465a0_mrs.bin /home/huyheo/work/tftpboot/t51/")
    print "Done"

def build_release_print():
    print "### Build Image"
    print "change to Dir: " + home_url + "release_buildtree/misc/buildsys"
    os.chdir(home_url + "release_buildtree/misc/buildsys")

    print "Build:"
    os.system("./humax_gen_squashfs_for_release_tree.sh release_print")

    print "### Copy to Tftp folder"
    print "cp /home/huyheo/work/Project/release_buildtree/misc/buildsys/../../bin/squashfs/release_print/vmlinuz-squashfs-73465a0_mrs.bin /home/huyheo/work/tftpboot/t51/"
    os.system("cp /home/huyheo/work/Project/release_buildtree/misc/buildsys/../../bin/squashfs/release_print/vmlinuz-squashfs-73465a0_mrs.bin /home/huyheo/work/tftpboot/t51/")

    print "Done"

if sys.argv[1] == 'debug':
    print 'Build debug image'
    build_debug()
elif sys.argv[1] =='release_print':
    build_release_print()
elif sys.argv[1] =='release':
    build_release()
elif target_file == 'help':
    print 'help'
