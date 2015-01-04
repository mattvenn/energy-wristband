#!/usr/bin/env python

import socket
import time
import pickle


class UDP_send():
    def __init__(self,logging, ip='192.168.0.255', port=50000):
        self.ip = ip
        self.logger = logging
        self.port = port
        self.sock = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_DGRAM)  # UDP
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def send(self, start, end, seq):
        message = {'start': start, 'end': end, 'seq': seq}
        data = pickle.dumps(message)

        self.logger.info("send [%d,%d,%d] to %s:%d" % 
                            (start, end, seq, self.ip, self.port))
        self.sock.sendto(data, (self.ip, self.port))

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)
    u = UDP_send(logging)

    for seq in range(4):
        u.send(1, 4, time.time())
        time.sleep(1)
