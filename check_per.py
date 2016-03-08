#!/usr/bin/python
#############################################
#Check_per
#Check if permission is configured correctly
#############################################

import os, stat

print '..start '
HOME_DIR ='/home/huyheo/work/Project/SUHD1_LHCR/platform/initram_rootfs/'



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
    os.chdir(os.path.join(HOME_DIR,path))
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
for data in to_check_per:
    check_per_info(data[0], data[1], data[2])


