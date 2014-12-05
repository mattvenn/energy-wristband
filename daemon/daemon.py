#!/usr/bin/env python
import threading
import time
import re
import signal
import serial
import send
import diff_realtime
from xively import xively

#for xively
feed_id = "130883"
meter_port = "/dev/ttyUSB0"
serial_debug = False

import logging

# set up logging to file - see previous section for more details
log_format = '%(asctime)s %(name)-10s %(levelname)-8s %(message)s'
logging.basicConfig(level=logging.DEBUG,
    format=log_format,
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

class SerialException(Exception):
    pass

def parse_msg(msg):
    m = re.search( "<tmpr>(\d+\.\d+)</tmpr>.*<watts>(\d+)</watts>", msg)
    if m != None:
        if m.group(1) and m.group(2):
            return float(m.group(1)),float(m.group(2))
    return None,None

def read_serial():
    if not serial_debug:
        serial_port = serial.Serial()
        serial_port.port=meter_port
        serial_port.baudrate=57600
        serial_port.timeout=10
        serial_port.open()
        serial_port.flushInput()


        #this times out
        logger.info("opened serial with %ds timeout" % serial_port.timeout)
        msg = serial_port.readline()

        serial_port.close()
    else:
        time.sleep(1)
        msg = None
        msg = '<msg><src>CC128-v0.11</src><dsb>00591</dsb><time>03:01:16</time><tmpr>15.7</tmpr><sensor>0</sensor><id>00077</id><type>1</type><ch1><watts>02777</watts></ch1></msg>'

    if msg:
        return parse_msg(msg)
    else:
        raise SerialException


#main loop
while True:
    try:
        (temp,power) = read_serial()
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

        logger.info("updating xively")
        xively_t = xively(feed_id,logging)
        xively_t.add_datapoint('temperature', temp)
        xively_t.add_datapoint('energy', power)
        xively_t.start()
        xively_t.join()
        logger.info("xively thread ended")
    except SerialException:
        logger.info("got nothing from meter")
