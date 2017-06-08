#!/usr/bin/python
print '...'
import os
import sys

make_url = "/home/huyheo/work/Project/FGDL/make"

print "### cd "+ make_url
os.chdir(make_url)

print "make fgdl"
os.system("make fgdl")
print "cp /home/huyheo/work/Project/FGDL/make/image/debug/rom2.elf  /home/huyheo/work/tftpboot/t51/"
os.system("cp /home/huyheo/work/Project/FGDL/make/image/debug/rom2.elf  /home/huyheo/work/tftpboot/t51/")



