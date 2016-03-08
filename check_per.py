#!/usr/bin/python
#############################################
#Check_per
#Check if permission is configured correctly
#############################################

import os, stat

print '..start '
HOME_DIR='/home/huyheo/work/SUHD1_CLEAN_CO'
INITRAM_DIR ='platform/initram_rootfs/'
BUSY_BOX_DIR="product_config/platform/oe_rootfs_source/suhd1/debug/meta-stm/meta-stm-bsp/recipes-humax/busybox/busybox/busybox.cfg"

INITRAM_DIR = os.path.join(HOME_DIR,INITRAM_DIR)
BUSY_BOX_DIR= os.path.join(HOME_DIR,BUSY_BOX_DIR)


to_check_per=[
#FP03
['firmware','0555', 'lib'],
['modules','0555', 'lib'],
['RT2860STA_conduct.dat','0555', 'etc/Wireless/RT2860STA'],
['RT2860STA.dat','0555', 'etc/Wireless/RT2860STA'],
['RT30xxEEPROM.bin','0555', 'etc/Wireless/RT2860STA'],
['audio_firmware-ID_2752_profileaudio-stih418-2GB-38.3.0.7-0.elf','0555', 'lib/firmware'],
['pti_tp5.elf','0555', 'lib/firmware'],
['MxL_5xx_FW.mbin','0555', 'lib/firmware'],
['vid_firmware-17.0-0-ID_2751_profilevideo-H418-stih418.elf','0555', 'lib/firmware'],
['bluetoothd','0555', 'usr/lib/bluez5/bluetooth'],
['dbus-daemon-launch-helper','0555', 'usr/lib/dbus'],
['fdma2_monaco_fdma0-v1.0.elf','0555', 'lib/firmware'],
['fdma2_monaco_fdma1-v1.0.elf','0555', 'lib/firmware'],
['fdma2_monaco_fdma2-v1.0.elf','0555', 'lib/firmware'],
['lpm-fw-STiH418_1.9.4.elf','0555', 'lib/firmware'],
['pti_memdma_h407_one-pkt-dac.elf','0555', 'lib/firmware'],
['tee_firmware-stih418_gp0_2G.elf','0555', 'lib/firmware'],
['tee_firmware-stih418_gp0_2G_HDCP2.elf','0555', 'lib/firmware'],
#FP04 
# missing file in ~/work/Project/SUHD1_LHCR/platform/initram_rootfs/lib/modules/3.10.65-stih418_family
['Licenses.txt', '0440', 'NDS'],
['emmc_partition.cfg', '0440', 'root'],
['start-profile.inc', '0440', 'NDS'],
['start-platform.inc', '0440', 'NDS'],
#FP20
['lib', '0755', 'var']

]

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

#BUSYBOX
check_list=[ 
        ['CONFIG_SHOW_USAGE','n'],
        ['CONFIG_LONG_OPTS','n'],
        ['CONFIG_FEATURE_SUID','n'],
        ['CONFIG_FEATURE_SUID_CONFIG','n'],
        ['CONFIG_FEATURE_SUID_CONFIG_QUIET','n'],
        ['CONFIG_FEATURE_SYSLOG','n'],
        ['CONFIG_FEATURE_RTMINMAX','n'],
        ['CONFIG_FEATURE_EDITING','n'],
        ['CONFIG_FEATURE_EDITING_SAVEHISTORY','n'],
        ['CONFIG_FEATURE_EDITING_FANCY_PROMPT','n'],
        ['CONFIG_AR','n'],
        ['CONFIG_DPKG_DEB','n'],
        ['CONFIG_FEATURE_DPKG_DEB_EXTRACT_ONLY','n'],
        ['CONFIG_CHGRP','n'],
        ['CONFIG_ECHO','n'],
        ['CONFIG_FEATURE_FANCY_ECHO','n'],
        ['CONFIG_ENV','n'],
        ['CONFIG_EXPR','n'],
        ['CONFIG_EXPR_MATH_SUPPORT_64','n'],
        ['CONFIG_FEATURE_LS_COLOR','n'],
        ['CONFIG_MKNOD','n'],
        ['CONFIG_PRINTF','n'],
        ['CONFIG_SYNC','n'],
        ['CONFIG_FEATURE_AUTOWIDTH','n'],
        ['CONFIG_FEATURE_HUMAN_READABLE','n'],
        ['CONFIG_VI','n'],
        ['CONFIG_ADDUSER','n'],
        ['COFNIG_FEATURE_ADDUSER_LONG_OPTIONS','n'],
        ['COFNIG_ADDGROUP','n'],
        ['COFNIG_FEATURE_ADDGROUP_LONG_OPTIONS','n'],
        ['CONFIG_DELUSER','n'],
        ['CONFIG_DELGROUP','n'],
        ['COFNIG_GETTY','n'],
        ['CONFIG_LOGIN','n'],
        ['CONFIG_PASSWD','n'],
        ['CONFIG_SU','n'],
        ['CONFIG_SULOGIN','n'],
        ['CONFIG_VLOCK','n'],
        ['CONFIG_CHATTR','n'],
        ['CONFIG_RMMOD','n'],
        ['CONFIG_DMESG', 'n'],
        ['CONFIG_FEATURE_DEMESG_PRETTY', 'n'],
        ['CONFIG_FDISK', 'n'],
        ['CONFIG_FEATURE_FDISK_WRITABLE', 'n'],
        ['CONFIG_MKSWAP', 'n'],
        ['CONFIG_FEATURE_MOUNT_FSTAB', 'n'],
        ['CONFIG_SWAPONOFF', 'n'],
        ['CONFIG_FEATURE_SWAPON_PRI', 'n'],
        ['CONFIG_UMOUNT', 'n'],
        ['CONFIG_FEATURE_UMOUNT_ALL', 'n'],
        ['CONFIG_LESS', 'n'],
        ['CONFIG_MICROCOM', 'n'],
        ['CONFIG_STRINGS', 'n'],
        ['CONFIG_NC', 'n'],
        ['COFNIG_BRCTL', 'n'],
        ['CONFIG_HTTPD', 'n'],
        ['CONFIG_IP', 'n'],
        ['CONFIG_NETSTAT', 'n'],
        ['CONFIG_TRACEROUTE', 'n'],
        ['CONFIG_TOP', 'n'],
        ['CONFIG_UPTIME', 'n'],
        ['CONFIG_FUSER', 'n'],
        ['CONFIG_BB_SYSCTL', 'n'],
        ['CONFIG_WATCH', 'n']
        ]

busybox_applet=[
        'ar',
        'brctl',
        'chmod',
        'chown',
        'chrt',
        'chvt',
        'deallocvt',
        'delgroup',
        'deluser',
        'dmesg',
        'dnsdomainname',
        'dpkg-deb',
        'dumpkmap',
        'env',
        'expr',
        'fgrep',
        'flock',
        'fuser',
        'getty',
        'httpd',
        'ifconfig',
        'ifdown',
        'ip',
        'loadfont',
        'loadkmap',
        'logger',
        'logname',
        'losetup',
        'lsmod',
        'microcom',
        'mkswap',
        'modprobe',
        'nc',
        'netstat',
        'openvt',
        'patch',
        'pivot_root',
        'rdate',
        'reset',
        'rfkill',
        'rmmod',
        'run-parts',
        'seq',
        'setconsole',
        'setsid',
        'sulogin',
        'switch_root',
        'top',
        'touch',
        'tty',
        'vi',
        'watch'
        ]

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







