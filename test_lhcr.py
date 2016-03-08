#!/usr/bin/python
#############################################
# Test LHCR implementation 
# Step:
# - configure HOME_DIR to your local repository
# - make hardening (refer to project page for make process)
# - configure INITRAM_DIR , BUSY_BOX_DIR 
# - Run test: sudo ./test_per.py
# - github: https://help.github.com/articles/adding-an-existing-project-to-github-using-the-command-line/
#############################################

import os, stat
from config import *

print '..start '



def get_per(path, name):
    os.chdir(os.path.join(INITRAM_DIR,path))
    per_info = oct(stat.S_IMODE(os.lstat(name).st_mode))
    return per_info

def check_per_info(name, required_per, path):
    #os.chdir(path)
    per_info = get_per(path, name)

    if per_info == required_per:
        print 'OK. Permission of: ', name,'is:', per_info
    else:
        print 'ERROR: File',name,'',required_per,'(required) diff ' , per_info




#################
#main
#################
#FP03, FP20, FP40
print'#############################################'
print'# Check Permission ' 
print'#############################################'
for data in to_check_per:
    check_per_info(data[0], data[1], data[2])

print'FP04\n'
#FP04 . Check all text, binary file per at ~/work/Project/SUHD1_LHCR/platform/initram_rootfs/lib/modules/3.10.65-stih418_family
#Check text file
print 'Check Text and bin file'
for root, dirs, files in os.walk(os.path.join(INITRAM_DIR,"lib/modules/3.10.65-stih418_family")):
        for file in files:
            if file.endswith(".txt"):
                print 'Text file:'
                print file

            if file.endswith(".bin"):
                path_info= os.path.abspath(os.path.join(root, file))
                #print file 
                os.chdir(root)
                per_info = oct(stat.S_IMODE(os.lstat(file).st_mode)) 
                print file, 'has', per_info

print'#############################################'
print'# Check busybox cfg file'
print'#############################################'
with open(BUSY_BOX_DIR) as f:
    content = f.readlines()
for cfg_info in check_list:
    flag=0
    for line in content:
        if cfg_info[0] in line:
            flag =1
            pos = line.find("=")
            if line[pos:].find(cfg_info[1]) >0:
                print 'OK', cfg_info[0],'=', cfg_info[1]
            else:
                print 'ERROR', cfg_info[0],'!=', cfg_info[1]
    if not flag:
        #print 'NOT DEFINE', cfg_info[0]
        pass
print'#############################################'
print'# Check busybox applets'
print'#############################################'
os.chdir(os.path.join(INITRAM_DIR,'usr/bin'))
for applet in busybox_applet:
    if os.path.isfile(applet):
        print'ERROR:',applet,'should be removed'
    else:
        print'OK:',applet,'is not included'







