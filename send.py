#!/usr/bin/env python

import os
import sys
import signal

ble_mac = "E4:E2:39:0A:C5:A9"
ble_host = 'hci0'

def handler(signum, frame):
    print 'Signal handler called with signal', signum
    raise IOError("Couldn't open device!")

#read buffer with this
#/usr/bin/gatttool -b E4:E2:39:0A:C5:A9 -t random --char-read --handle=0x000e

def send_energy(energy):
    energy = int(energy * 255)
    SEND = hex(energy)[2:].zfill(2)
    cmd = "/usr/bin/gatttool -i " + ble_host + " -b " + ble_mac + " --char-write --handle=0x0011 --value=" + SEND
    print(cmd)

    #Set the signal handler and alarm
    import subprocess
    proc = subprocess.Popen(cmd.split())
    import time
    time.sleep(0.5)
    returncode = proc.poll()
    if returncode == 0:
        print("success")
    elif returncode == None:
        #hung
        print("hung")
        proc.terminate()

if __name__ == '__main__':
    #from 0 to 1
    energy = sys.argv[1]
    energy = float(energy)
    send_energy(energy)

