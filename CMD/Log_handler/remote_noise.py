import os, sys
print "remote noise"
print 'sys.argv[1] = ', sys.argv[1]
print 'sys.argv[2] = ', sys.argv[2]
try:
    target_file  = sys.argv[1]
except:
    print 'Need info of Type: debug or release'
    exit()

try:
    out_put_file = sys.argv[2]
except:
    print 'No Binary name.  Ex: T51_73535_CDI_24Feb2017_R11052.tar.bz2'
    exit()

f= open(target_file,"r")
lines = f.readlines()
f.close()
f = open(out_put_file,"w")
for line in lines:
    #if line.find("USER_INPUT_KEY_BACK") >0:
    if line.find("ioctl") >0:
        print "find\n line=", line
        f.write(line)
    else:
        print 'remote line=', line
    

f.close()

