# !/usr/bin/env python

import sys
import threading
import subprocess
import time


class wristband():

    ble_mac = "E4:E2:39:0A:C5:A9"
    ble_mac = "E1:40:D8:62:ED:1A"  # other rfduino
    ble_host = 'hci0'
    gatt = "./gatttool"

    def __init__(self, logging, timeout=6):
        self.timeout = timeout
        self.logger = logging.getLogger('bluetooth')
        self.base_cmd = wristband.gatt + " -t random -i " + \
            wristband.ble_host + " -b " + wristband.ble_mac

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

        if data:
            # expecting 4 bytes for each int sent
            if len(data.split()) == 2 + 4 + 4:

                # unpack
                batt_adc = self.unpack(data, 0)
                uptime = self.unpack(data, 1)

                # convert batt
                vcc = 3.3  # should be 3.3
                batt_level = batt_adc / 1023.0 * vcc * 2

                self.logger.info("batt = %.2fv uptime = %ds" % (batt_level, uptime))
                return(batt_level, uptime)
            else:
                raise ValueError("problem parsing data: " + data)
        else:
            raise ValueError("got no data")

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
        else:
            # an error?
            self.logger.warning("unexpected return code from gatttool: %d" % returncode)


if __name__ == '__main__':
    # from 0 to 1
    start = int(sys.argv[1])
    end = int(sys.argv[2])
    import logging
    logging.warning("starting")
    s = wristband(logging)
    s.send(start, end)
    s.get()
