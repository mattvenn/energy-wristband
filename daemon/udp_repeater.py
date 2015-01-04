#!/usr/bin/env python

import socket
import time
import pickle


class UDP_get():
    def __init__(self,logging, port=50000):
        self.logger = logging
        self.port = port
        self.sock = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_DGRAM)  # UDP

    def listen(self):
        self.logger.info("binding to port %d" % (self.port))
        self.sock.bind(('', self.port))
        while True:
            data, addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes
            msg = pickle.loads(data)
            self.logger.info("got [%d,%d,%d] from %s" % (
                msg["start"], msg["end"], msg["seq"], addr))
            try:
                # send start and end
                s = wristband(logging, args.address,
                    timeout = args.timeout)
                s.send(msg["start"], msg["end"])

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

    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)

    u = UDP_get(logging, port=args.port)

    #start
    u.listen()

