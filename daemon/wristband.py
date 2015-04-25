#!/usr/bin/env python

import sys, time
from easyprocess import Proc
import plugins.udp_send as udp_send
import logging

log = logging.getLogger(__name__)

class WB_Exception(Exception):
    def __init__(self, message):
        super(WB_Exception, self).__init__(message)
        self.message = message

class wristband():

    ble_host = 'hci0'
    gatt = "/usr/bin/gatttool"

    def __init__(self, ble_address, timeout=10, udp_repeat=False):
        self.timeout = timeout
        if ble_address is None:
            raise WB_Exception("no BLE address given")
        log.info("address = %s" % ble_address)
        self.base_cmd = wristband.gatt + " -t random -i " + \
            wristband.ble_host + " -b " + ble_address

        self.seq = 0
        self.udp_repeat = udp_repeat
        if self.udp_repeat:
            self.udp = udp_send.UDP_send()

    def re_send(self, start):
        # send out on udp
        if self.udp_repeat:
            self.udp.re_send(start)

        log.info("sending %d" % start)
        send = hex(start)[2:].zfill(2)
        cmd = self.base_cmd + " --char-write --handle=0x0011 --value=" + send
        self.run_command(cmd)

    def send(self, start, end, seq=None):
        # seq is to avoid repeated warnings with udp repeaters
        # it can either be provided, or will be generated using
        # last 3 digits of current time expressed in seconds
        # can only be up to one byte
        if seq is None:
            seq = int(str(int(time.time()))[-3:]) % 255

        # send out on udp
        if self.udp_repeat:
            self.udp.send(start, end, seq)

        log.info("sending %d %d %d to wristband" % (start, end, seq))
        send = hex(start)[2:].zfill(2) + \
            hex(end)[2:].zfill(2) + hex(seq)[2:].zfill(2)
        cmd = self.base_cmd + " --char-write --handle=0x0011 --value=" + send
        self.run_command(cmd)

    def unpack(self, data, int_num):
        offset = int_num * 4 + 2
        byte2 = data.split()[offset]
        byte1 = data.split()[offset+1]
        hex_val = byte1 + byte2
        return int(hex_val, 16)

    def get(self):
        log.info("requesting data")
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

            log.info("raw = %d batt = %.2fv uptime = %ds" %
                            (batt_adc, batt_level, uptime))
            return(batt_level, uptime)
        else:
            raise WB_Exception("problem parsing data: " + data)

    def run_command(self, cmd):
        log.info("waiting %d seconds for process" % self.timeout)
        log.debug(cmd)

        # run with easyprocess
        proc=Proc(cmd).call(timeout=self.timeout)

        if proc.return_code == 0:
            log.info("success")
            return proc.stdout
        elif proc.return_code == -15:
            # timed out
            raise WB_Exception("gatttool timed out")
        else:
            # an error?
            raise WB_Exception("gatttool returned error: %s" % proc.stderr)



if __name__ == '__main__':
    import argparse
    from ConfigParser import ConfigParser, NoSectionError
    config = ConfigParser()
    config.read('config.rc')
    d_ble_address = config.get('ble', 'address')
    d_ble_timeout = config.get('ble', 'timeout')

    parser = argparse.ArgumentParser(description="read meter, post to internet and send to energy wristband")
    parser.add_argument('--timeout', action='store', type=int, 
        help="timeout for gatttool", default=d_ble_timeout)
    parser.add_argument('--start', action='store', type=int, 
        help="start", default=1)
    parser.add_argument('--resend', action='store_const', const=True,
        help="update instead of alert", default=False)
    parser.add_argument('--end', action='store', type=int, 
        help="end", default=4)
    parser.add_argument('--address', help="BLE address of wristband",
        default = d_ble_address)
    parser.add_argument('--udp_repeat', action='store_const', const=True,
        default=False,
        help="increase coverage by broadcasting via UDP to other computers")
    

    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)

    try:
        # send start and end
        s = wristband(args.address, udp_repeat=args.udp_repeat,
                        timeout = args.timeout)
        if args.resend:
            s.re_send(args.start)
        else:
            s.send(args.start, args.end)

        # get battery level and uptime
        s.get()
    except WB_Exception as e:
        log.error(e)
