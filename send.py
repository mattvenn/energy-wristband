#!/usr/bin/env python

import os
import sys
import signal

ble_mac = "E4:E2:39:0A:C5:A9"
ble_mac = "E1:40:D8:62:ED:1A" #other rfduino
ble_host = 'hci0'

def handler(signum, frame):
    print 'Signal handler called with signal', signum
    raise IOError("Couldn't open device!")

#read buffer with this
#/usr/bin/gatttool -b E4:E2:39:0A:C5:A9 -t random --char-read --handle=0x000e

def send_energy(start,end):
    #energy = int(energy * 255)
    SEND = hex(start)[2:].zfill(2) + hex(end)[2:].zfill(2) 
    if os.uname()[1] == 'mattsmac':
        random = '-t random'
    else:
        random = ''
    cmd = "/usr/bin/gatttool -i " + ble_host + " -b " + ble_mac + random + " --char-write --handle=0x0011 --value=" + SEND
    print(cmd)
    do_send(cmd)

def get_battery():
    cmd = "/usr/bin/gatttool -i " + ble_host + " -b " + ble_mac + " -t random --char-read --handle=0x000e"
 # second byte then first byte to get int
 #   int("02e1", 16)

def do_send(cmd):
    #Set the signal handler and alarm
    import subprocess
    proc = subprocess.Popen(cmd.split())
    import time
    time.sleep(6.0)
    returncode = proc.poll()
    if returncode == 0:
        print("success")
    elif returncode == None:
        #hung
        print("hung")
        proc.terminate()

if __name__ == '__main__':
    #from 0 to 1
    start = int(sys.argv[1])
    end = int(sys.argv[2])
    send_energy(start,end)

