#!/usr/bin/env python

import sys
import threading
import subprocess
import time


class wristband():

    ble_mac = "E4:E2:39:0A:C5:A9"
    ble_mac = "E1:40:D8:62:ED:1A"  # other rfduino
    ble_mac = "E7:2C:35:BC:D2:B9"  # wb module
    ble_host = 'hci0'
    gatt = "./gatttool"

    def __init__(self, logging, timeout=10):
        self.timeout = timeout
        self.logger = logging.getLogger('bluetooth')
        self.base_cmd = wristband.gatt + " -t random -i " + \
            wristband.ble_host + " -b " + wristband.ble_mac

    def re_send(self, start):
        self.logger.info("sending %d" % start)
        send = hex(start)[2:].zfill(2)
        cmd = self.base_cmd + " --char-write --handle=0x0011 --value=" + send
        self.run_command(cmd)

    def send(self, start, end):
        self.logger.info("sending %d %d" % (start, end))
        send = hex(start)[2:].zfill(2) + hex(end)[2:].zfill(2)
        cmd = self.base_cmd + " --char-write --handle=0x0011 --value=" + send
        self.run_command(cmd)

    def unpack(self, data, int_num):
        offset = int_num * 4 + 2
        byte2 = data.split()[offset]
        byte1 = data.split()[offset+1]
        hex_val = byte1 + byte2
        return int(hex_val, 16)

    def get(self):
        self.logger.info("requesting data")
        cmd = self.base_cmd + " --char-read --handle=0x000e"
        data = self.run_command(cmd)

        # expecting 4 bytes for each int sent
        if len(data.split()) == 2 + 4 + 4:

            # unpack
            batt_adc = self.unpack(data, 0)
            uptime = self.unpack(data, 1)

            # convert batt
            a_in = batt_adc * 1.2 / 1023
            R1 = 76000.0  # should be 100k but adjusted for RAIN impedance
            R2 = 226000.0
            batt_level = a_in / (R1 / (R1+R2))
            batt_level = round(batt_level, 2)

            self.logger.info("raw = %d batt = %.2fv uptime = %ds" %
                            (badd_adc, batt_level, uptime))
            return(batt_level, uptime)
        else:
            raise ValueError("problem parsing data: " + data)

    def run_command(self, cmd):
        proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        self.logger.info("waiting %d seconds for process" % self.timeout)
        self.logger.debug(cmd)

        # wait
        time.sleep(self.timeout)

        # see if command is still running
        returncode = proc.poll()
        if returncode == 0:
            self.logger.info("success")
            data = proc.stdout.readline()
            return data
        elif returncode is None:
            # hung
            self.logger.warning("hung")
            proc.terminate()
            raise ValueError("gatttool timed out")
        else:
            # an error?
            raise ValueError("unexpected return code from gatttool: %d" % returncode)


if __name__ == '__main__':
    # from 0 to 1
    start = int(sys.argv[1])
    end = int(sys.argv[2])
    import logging
    logging.basicConfig(level=logging.DEBUG)
    s = wristband(logging)
    s.send(start, end)
    # (batt_level, uptime ) = s.get()
    # logging.warning("got %fv %ds" % (batt_level, uptime))
