#!/usr/bin/env python
import threading
import time
import re
import signal
import serial
import send
from differentiator import diff_realtime
import CosmFeedUpdate as cosm

#private key stored in a file
keyfile="api.key"
key=open(keyfile).readlines()[0].strip()
feed_id = "130883"

feed_id = "130883"

meter_port = "/dev/ttyUSB0"
import logging

# set up logging to file - see previous section for more details
log_format = '%(asctime)s %(name)-10s %(levelname)-8s %(message)s'
logging.basicConfig(level=logging.DEBUG,
    format=log_format,
#    datefmt='%m-%d %H:%M',
    filename='reader.log',
    filemode='w')

# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter(log_format)
console.setFormatter(formatter)
# add the handler to the root logger
logger = logging.getLogger('')
logger.addHandler(console)

def parse_msg(msg):
    m = re.search( "<tmpr>(\d+\.\d+)</tmpr>.*<watts>(\d+)</watts>", msg)
    if m != None:
        if m.group(1) and m.group(2):
            return float(m.group(1)),float(m.group(2))
    return None,None

def read_serial():
    serial_port = serial.Serial()
    serial_port.port=meter_port
    serial_port.baudrate=57600
    serial_port.timeout=10
    serial_port.open()
    serial_port.flushInput()
    logger.info("opened serial with %ds timeout" % serial_port.timeout)

    #this times out
    msg = serial_port.readline()
    serial_port.close()

    #print(msg)
    if msg:
        return parse_msg(msg)
    return None,None

class reader(threading.Thread):

    def __init__(self,timeout=1):
        threading.Thread.__init__(self)
        self.timeout = timeout
        self.success = False

    def run(self):
        print "thread started"

        #finish

#s = reader()
#s.start()
#s.join()
#if s.success:
#    print s.power, s.temp

while True:
    (temp,power) = read_serial()

    if power:


        logger.info("meter returned %f W %f C" % (power,temp))
        (last,this) = diff_realtime.diff(power,logging)
        if last != None:
            s = send.send(last,this,logging)
            logger.info("start thread for bluetooth")
            s.start()
            #don't join here, have a queue
            s.join()
            logger.info("bluetooth thread ended")
        else:
            logger.info("not enough difference")

        logger.info("xively thread")
        pfu = cosm.CosmFeedUpdate(feed_id,key,logging)
        pfu.addDatapoint('temperature', temp)
        pfu.addDatapoint('energy', power)
        # finish up and submit the data
        pfu.buildUpdate()
        pfu.start()
        #don't join here, have a queue
        pfu.join()
        logger.info("xively thread ended")
    else:
        logger.info("got nothing from meter")
