#!/usr/bin/python
print '...'
import os
import sys

home_url = "."
#home_url = "/home/huyheo/work/Project/T51"

try:
	target_file = sys.argv[1]
	target2 = sys.argv[2]
except:
	print 'no input parameter.'




#########################
# clean checkout
# make world
##########################*/
def clean_build():
	"""
    print "### cd "+ home_url  
    if (os.path.isdir(home_url)):
        print 'Folder is existed.'
        os.system("sudo rm -fr " + home_url)
   
	 
    os.system("mkdir " + home_url)

    print "move to " + home_url
    os.chdir(home_url)

    print " svn co http://svn.humaxdigital.com/drr_cdi/trunk/models/t51/ ./"
    os.system("svn co http://svn.humaxdigital.com/drr_cdi/trunk/models/t51/ ./")
   
    #new_home_url = os.path.join(home_url,"hdr-1002s-ph3")
	"""

	print "git clone ssh://git.humaxdigital.com/git/HA/app/external/micom_3rdparty/3rd_party_sdk.git -b p_dolphinplus_bhmc 3rd_party"

	os.system("git clone ssh://git.humaxdigital.com/git/HA/app/external/micom_3rdparty/3rd_party_sdk.git -b p_dolphinplus_bhmc 3rd_party")

	print "git clone ssh://git.humaxdigital.com/git/HA/app/micom/build.git -b p_dolphinplus_bhmc build"
	os.system("git clone ssh://git.humaxdigital.com/git/HA/app/micom/build.git -b p_dolphinplus_bhmc build")

	print "git clone ssh://git.humaxdigital.com/git/HA/app/micom/humax.git -b p_dolphinplus_bhmc source/humax"
	os.system("git clone ssh://git.humaxdigital.com/git/HA/app/micom/humax.git -b p_dolphinplus_bhmc source/humax")

	print "git clone ssh://git.humaxdigital.com/git/HA/platform/system/micom/tcc/tcc803x_upgrader.git -b p_dolphinplus_bhmc source/tcc_upgrader"
	os.system("git clone ssh://git.humaxdigital.com/git/HA/platform/system/micom/tcc/tcc803x_upgrader.git -b p_dolphinplus_bhmc source/tcc_upgrader")

	print "git clone ssh://git.humaxdigital.com/git/HA/platform/system/micom/tcc/tcc803x.git -b p_dolphinplus_bhmc source/sdk"
	os.system("git clone ssh://git.humaxdigital.com/git/HA/platform/system/micom/tcc/tcc803x.git -b p_dolphinplus_bhmc source/sdk")
	print "git clone ssh://git.humaxdigital.com/git/ha/applications/shared_env.git -b p_dolphinplus_bhmc source/shared_env"
	os.system("git clone ssh://git.humaxdigital.com/git/ha/applications/shared_env.git -b p_dolphinplus_bhmc source/shared_env")
  	print "git clone ssh://git.humaxdigital.com/git/ha/toolchains/tcc803x/tcc803x_r5_toolchain.git -b h_hyundai_dn8c utils/toolchain"
   	os.system("git clone ssh://git.humaxdigital.com/git/ha/toolchains/tcc803x/tcc803x_r5_toolchain.git -b h_hyundai_dn8c utils/toolchain")
 	print "git clone ssh://git.humaxdigital.com/git/HA/app/micom/document.git -b p_dolphinplus_bhmc document"
 	os.system("git clone ssh://git.humaxdigital.com/git/HA/app/micom/document.git -b p_dolphinplus_bhmc document")


	



"""
if sys.argv[1] == 'clean':
    clean_build(sys.argv[2])
if sys.argv[2]:
    clean_build(sys.argv[2])
elif target_file == 'help':
    print 'help'
"""
if 1:
    clean_build()
    
