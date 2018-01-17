#!/usr/bin/python
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

def refine_data(line):
    data = line.split(" ")
    data3= data[2].replace(':', '.')
    data4 = data3.replace(']','')
    data5 = data4[0:8]
    print 'data5', data5
    data6 = data5.split('.')
    data7 = int(data6[0])*60*60 + int(data6[1])*60 + int(data6[2])
    print 'data7 = ', data7
    return data7


#refine_data("[16/01/18 - 14:41:12:692] Restarting system.")

f= open(target_file,"r")
lines = f.readlines()
f.close()
f = open(out_put_file,"w")
duration1=0
duration2=0
result_info =0
for line in lines:
    #if line.find("USER_INPUT_KEY_BACK") >0:
    if line.find("Restarting system") >0:
        print "find\n line=", line
        if duration1 ==0:
            duration1 = refine_data(line)
        elif duration1:
            duration2 = refine_data(line)
            result_info = duration2 - duration1
            print ' The gap is ', result_info
            duration1 = 0
            duration2 = 0
            line = "duration = "+ str(result_info) + "\n"
            f.write(line)
    else:
        print 'remote line=', line
    

f.close()

