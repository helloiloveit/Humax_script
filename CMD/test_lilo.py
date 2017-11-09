#!/usr/bin/python
print '...'
import os
import sys

make_url = "/home/huyheo/work/Project/LILO/make"
def_config_url = "/home/huyheo/work/Project/LILO/product_config/defconfig"

build_lilo_url = " /home/huyheo/work/Project/LILO/make/image/lilo.bin"
target_lilo_debug_url = "/home/huyheo/work/Project/release_buildtree/misc/lilo/debug"
target_lilo_release_url = "/home/huyheo/work/Project/release_buildtree/misc/lilo/release"
target_lilo_build = "/home/huyheo/work/Project/release_buildtree/misc/buildsys"
target_dev = "/home/huyheo/work/Project/Test_New_Co/make/mrsimage/debug"
target_dev_release = "/home/huyheo/work/Project/Test_New_Co/make/mrsimage/release"

def help_info():
    print '************Test LILO***********\n'
    print ' test_lilo.py   [Option] \n '
    print ' test_lilo.py debug \n'
    print ' test_lilo.py release \n'
    print '********************************\n'


try:
	target_file = sys.argv[1]
except:
    help_info()
    exit()


def test_lilo(version_info):
    print "### cd "+ make_url
    os.chdir(make_url)

    print "make clean "
    os.system("make clean ")
    if version_info =='debug':
        print "make t52_def.cfg "
        os.system("make t52_def.cfg ")
    elif version_info == 'release':
        print "make t52_release_def.cfg "
        os.system("make t52_def.cfg ")
    else:
        print ' ERRR wrong parameter'
    print "### cd "+ def_config_url
    os.chdir(def_config_url)

    print "cp  " + "humax_product_def.h" + " " + "../../include/"
    os.system("cp  " + "humax_product_def.h" + " " + "../../include/")
    print "cp  " + "humax_lilo_ref.h" + " " + "../../include/"
    os.system("cp  " + "humax_lilo_ref.h" + " " + "../../include/")

    print "### cd "+ make_url
    os.chdir(make_url)
    print "imake make_lilo "
    os.system("make make_lilo ")


    #print "cp   " + build_lilo_url + " " + target_lilo_debug_url
    #os.system("cp   " + build_lilo_url + " " + target_lilo_debug_url)
    #os.system("cp   " + build_lilo_url + " " + target_lilo_release_url)

    print "cp   " + build_lilo_url + " " + target_dev
    print "cp   " + build_lilo_url + " " + target_dev_release
    os.system("cp   " + build_lilo_url + " " + target_dev)
    os.system("cp   " + build_lilo_url + " " + target_dev_release)

    tftp_dir ="/home/huyheo/work/tftpboot/t51"
    print "cp   " + build_lilo_url + " " + tftp_dir
    os.system("cp   " + build_lilo_url + " " + tftp_dir)



"""
print target_lilo_build
os.chdir(target_lilo_build)

print "./humax_gen_squashfs_for_release_tree.sh " + "release_print"
os.system("./humax_gen_squashfs_for_release_tree.sh " + "release_print")


print "### Copy to Tftp folder"
print "cp /home/huyheo/work/Project/release_buildtree/misc/buildsys/../../bin/squashfs/release_print/vmlinuz-squashfs-73465a0_mrs.bin  /home/huyheo/work/tftpboot/t51"
os.system("cp /home/huyheo/work/Project/release_buildtree/misc/buildsys/../../bin/squashfs/release_print/vmlinuz-squashfs-73465a0_mrs.bin /home/huyheo/work/tftpboot/t51")
"""



if sys.argv[1] == 'debug':
    print 'Build debug image'
    test_lilo('debug')
elif sys.argv[1] =='release':
    test_lilo('release')
else:
    help_info()
