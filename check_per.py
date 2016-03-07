#!/usr/bin/python
#############################################
#Check_per
#Check if permission is configured correctly
#############################################

import os, stat

print '..start '
def get_per(path, name):
    os.chdir(path)
    per_info = oct(stat.S_IMODE(os.lstat(name).st_mode))
    return per_info


to_check_per=[
['start-profile.inc', '0440', '/home/huyheo/work/Project/SUHD1_LHCR/platform/initram_rootfs/NDS'],
['start-platform.inc', '0440', '/home/huyheo/work/Project/SUHD1_LHCR/platform/initram_rootfs/NDS'],
['firmware','0555', '/home/huyheo/work/Project/SUHD1_LHCR/platform/initram_rootfs/lib'],
['modules','0555', '/home/huyheo/work/Project/SUHD1_LHCR/platform/initram_rootfs/lib'],
['RT2860STA_conduct.dat','0555', '/home/huyheo/work/Project/SUHD1_LHCR/platform/initram_rootfs/etc/Wireless/RT2860STA'],
['RT2860STA.dat','0555', '/home/huyheo/work/Project/SUHD1_LHCR/platform/initram_rootfs/etc/Wireless/RT2860STA']
]




def check_per_info(name, required_per, path):
    os.chdir(path)
    per_info = get_per(path, name)

    if per_info == required_per:
        print 'OK. Permission of: ', name,'is:', per_info
    else:
        print 'ERROR: File',name, '..Required permission', required_per, 'is diff with', per_info




#################
#main
#################
for data in to_check_per:
    check_per_info(data[0], data[1], data[2])


