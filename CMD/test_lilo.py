#!/usr/bin/python
print '...'
import os
import sys

make_url = "/home/huyheo/work/Project/LILO/make"
build_lilo_url = " /home/huyheo/work/Project/LILO/make/image/lilo.bin"
target_lilo_url = "/home/huyheo/work/Project/release_buildtree/misc/lilo/debug"
target_lilo_build = "/home/huyheo/work/Project/release_buildtree/misc/buildsys"

print "### cd "+ make_url
os.chdir(make_url)

print "imake make_lilo "
os.system("make make_lilo ")


print "cp   " + build_lilo_url + " " + target_lilo_url
os.system("cp   " + build_lilo_url + " " + target_lilo_url)


print target_lilo_build
os.chdir(target_lilo_build)

print "./humax_gen_squashfs_for_release_tree.sh " + "debug"
os.system("./humax_gen_squashfs_for_release_tree.sh " + "debug")


print "### Copy to Tftp folder"
print "cp /home/huyheo/work/Project/release_buildtree/misc/buildsys/../../bin/squashfs/debug/vmlinuz-squashfs-73465a0_mrs.bin /home/huyheo/work/tftpboot/t51"
os.system("cp /home/huyheo/work/Project/release_buildtree/misc/buildsys/../../bin/squashfs/debug/vmlinuz-squashfs-73465a0_mrs.bin /home/huyheo/work/tftpboot/t51")

