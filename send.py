#!/usr/bin/env python

import os
import sys
import signal

ble_mac = "E4:E2:39:0A:C5:A9"
ble_mac = "E1:40:D8:62:ED:1A" #other rfduino
ble_host = 'hci0'

if os.uname()[1] == 'mattsmac':
    random = '-t random'
else:
    random = ''

def handler(signum, frame):
    print 'Signal handler called with signal', signum
    raise IOError("Couldn't open device!")

def send_energy(start,end):
    #energy = int(energy * 255)
    SEND = hex(start)[2:].zfill(2) + hex(end)[2:].zfill(2) 
    cmd = "/usr/bin/gatttool -i " + ble_host + " -b " + ble_mac + random + " --char-write --handle=0x0011 --value=" + SEND
    print(cmd)
    do_send(cmd)

def get_battery():
    cmd = "/usr/bin/gatttool -i " + ble_host + " -b " + ble_mac + random + " --char-read --handle=0x000e"
    data = do_send(cmd)
    #this check is broken: better to split and check num chunks
    if data:
        if len(data.split()) == 6:
            #got good value
            byte2 = data.split()[2]
            byte1 = data.split()[3]
            hex_val = byte1 + byte2
            int_val = int(hex_val,16)
            print(int_val)
            vcc = 3.3 #should be 3.3
            batt_level = int_val / 1023.0 * vcc * 2
            print("batt = %.2fv" % batt_level)
        else:
            print("problem with data: " + data)
    else:
        print("got no data")

def do_send(cmd):
    #Set the signal handler and alarm
    import subprocess
    proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    import time
    time.sleep(6.0)
    returncode = proc.poll()
    if returncode == 0:
        print("success")
        data = proc.stdout.readline() 
        return data
    elif returncode == None:
        #hung
        print("hung")
        proc.terminate()

if __name__ == '__main__':
    #from 0 to 1
    start = int(sys.argv[1])
    end = int(sys.argv[2])
    send_energy(start,end)
    get_battery()

