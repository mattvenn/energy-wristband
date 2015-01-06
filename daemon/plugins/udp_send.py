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

    def re_send(self, start):
        self.send_udp({'type': 'resend', 'start': start})

    # seq is to avoid repeated warnings with udp repeaters
    def send(self, start, end, seq):
        self.send_udp({'type': 'send', 'start': start, 'end': end,
                         'seq': seq})

    def send_udp(self, message):
        data = pickle.dumps(message)
        self.sock.sendto(data, (self.ip, self.port))
        self.logger.info("sent to %s:%d" % (self.ip, self.port))

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)
    u = UDP_send(logging)

    for seq in range(4):
        u.send(1, 4, time.time())
        time.sleep(1)
