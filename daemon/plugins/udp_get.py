#!/usr/bin/env python

import socket
import time
import pickle


class UDP_get():
    def __init__(self,logging, ip='192.168.0.9', port=5000):
        self.ip = ip
        self.logger = logging
        self.port = port
        self.sock = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_DGRAM)  # UDP

    def listen(self):
        self.logger.info("binding to %s:%d" % (self.ip, self.port))
        self.sock.bind((self.ip, self.port))
        while True:
            data, addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes
            msg = pickle.loads(data)
            self.logger.info("got [%d,%d,%d] from %s" % (
                msg["start"], msg["end"], msg["seq"], addr))

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)
    u = UDP_get(logging)
    u.listen()


