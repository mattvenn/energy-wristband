#!/usr/bin/env python

import sys
from easyprocess import Proc

class WB_Exception(Exception):
    def __init__(self, message):
        super(WB_Exception, self).__init__(message)
        self.message = message

class wristband():

    ble_host = 'hci0'
    gatt = "/usr/bin/gatttool"

    def __init__(self, logging, ble_address, timeout=10):
        self.timeout = timeout
        self.logger = logging.getLogger('bluetooth')
        self.logger.debug("address = %s" % ble_address)
        self.base_cmd = wristband.gatt + " -t random -i " + \
            wristband.ble_host + " -b " + ble_address

    def re_send(self, start):
        self.logger.info("sending %d" % start)
        send = hex(start)[2:].zfill(2)
        cmd = self.base_cmd + " --char-write --handle=0x0011 --value=" + send
        self.run_command(cmd)

    def send(self, start, end):
        self.logger.info("sending %d %d to wristband" % (start, end))
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
                            (batt_adc, batt_level, uptime))
            return(batt_level, uptime)
        else:
            raise WB_Exception("problem parsing data: " + data)

    def run_command(self, cmd):
        self.logger.info("waiting %d seconds for process" % self.timeout)
        self.logger.debug(cmd)

        # run with easyprocess
        proc=Proc(cmd).call(timeout=self.timeout)

        if proc.return_code == 0:
            self.logger.info("success")
            return proc.stdout
        elif proc.return_code == -15:
            # timed out
            raise WB_Exception("gatttool timed out")
        else:
            # an error?
            raise WB_Exception("gatttool returned error: %s" % proc.stderr)



if __name__ == '__main__':
    import argparse
    import logging

    parser = argparse.ArgumentParser(description="read meter, post to internet and send to energy wristband")
    parser.add_argument('--start', action='store', type=int, 
        help="start", default=1)
    parser.add_argument('--end', action='store', type=int, 
        help="end", default=4)
    parser.add_argument('--address', help="BLE address of wristband",
        default = None)

    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)

    # send start and end
    s = wristband(logging,args.address)
    s.send(args.start, args.end)

    # get battery level and uptime
    s.get()
