#!/usr/bin/env python

import socket
import time
import pickle
from wristband import wristband, WB_Exception



class UDP_get():
    def __init__(self,logging, port=50000):
        self.logger = logging
        self.port = port
        self.sock = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_DGRAM)  # UDP
        # send start and end
        self.wb = wristband(logging, args.address,
            timeout = args.timeout)

    def listen(self):
        self.logger.info("binding to port %d" % (self.port))
        self.sock.bind(('', self.port))
        while True:
            data, addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes
            msg = pickle.loads(data)
            self.logger.info("got a %s message from %s" % (msg["type"], addr))
            try:
                if msg["type"] == "send":
                    self.wb.send(msg["start"], msg["end"], msg["seq"])
                if msg["type"] == "resend":
                    self.wb.resend(msg["start"])

            except WB_Exception as e:
                logging.error(e)

if __name__ == '__main__':
    import argparse
    import logging

    parser = argparse.ArgumentParser(description="listen to UDP, pass on to wristband")
    parser.add_argument('--timeout', action='store', type=int, 
        help="timeout for gatttool", default=10)
    parser.add_argument('--port', action='store', type=int, 
        help="port", default=50000)
    parser.add_argument('--address', help="BLE address of wristband",
        default = None, required=True)
    parser.add_argument('-d','--debug',
        help='print lots of debugging statements',
        action="store_const", dest="loglevel", const=logging.DEBUG,
        default=logging.WARNING)
    parser.add_argument('-v','--verbose',
        help='be verbose',
        action="store_const", dest="loglevel", const=logging.INFO)

    args = parser.parse_args()

    # set up logging to file
    log_format = '%(asctime)s %(name)-10s %(levelname)-8s %(message)s'
    logging.basicConfig(level=args.loglevel,
                        format=log_format,
                        filename='repeater.log')

    repeater = UDP_get(logging, port=args.port)

    #start
    repeater.listen()

