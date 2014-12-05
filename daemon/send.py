#!/usr/bin/env python

import os
import sys
import threading
import subprocess
import time

ble_mac = "E4:E2:39:0A:C5:A9"
ble_mac = "E1:40:D8:62:ED:1A" #other rfduino
ble_host = 'hci0'

class send(threading.Thread):

    def __init__(self,start,end,logging,timeout=6):
        threading.Thread.__init__(self)
        self.start_p = start
        self.timeout = timeout
        self.end_p = end
        self.logger = logging.getLogger('bluetooth')
        self.logger.info("started with %d %d" % (start,end))


    def run(self):
        #energy = int(energy * 255)
        SEND = hex(self.start_p)[2:].zfill(2) + hex(self.end_p)[2:].zfill(2) 
        cmd = "/usr/bin/gatttool -i " + ble_host + " -b " + ble_mac + " -t random --char-write --handle=0x0011 --value=" + SEND
        self.logger.debug(cmd)
        self.do_send(cmd)
    
    def get_battery():
        cmd = "/usr/bin/gatttool -i " + ble_host + " -b " + ble_mac + " -t random --char-read --handle=0x000e"
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
    
    def do_send(self,cmd):
        #Set the signal handler and alarm
        proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        self.logger.info("waiting %d seconds for process" % self.timeout)
        time.sleep(self.timeout)
        returncode = proc.poll()
        if returncode == 0:
            self.logger.info("success")
            data = proc.stdout.readline() 
            return data
        elif returncode == None:
            #hung
            self.logger.info("hung")
            proc.terminate()
    
if __name__ == '__main__':
    #from 0 to 1
    start = int(sys.argv[1])
    end = int(sys.argv[2])
    s = sender(start,end)
    s.start()
    s.join()
    #get_battery()

