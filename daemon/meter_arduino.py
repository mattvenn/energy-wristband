import serial
import time
import re
import logging

log = logging.getLogger(__name__)
serial_debug = True

"""
use a simple arduino based power simulator for demos
"""

class Meter_Exception(Exception):
    def __init__(self, message):
        super(Meter_Exception, self).__init__(message)
        self.message = message

def read_meter(meter_port, timeout=10):
    if not serial_debug:
        serial_port = serial.Serial()
        serial_port.port = meter_port
        serial_port.baudrate = 9600
        serial_port.timeout = timeout
        serial_port.open()
        serial_port.flushInput()

        # this times out
        log.debug("opened serial with %ds timeout" % serial_port.timeout)
        msg = serial_port.readline()
        serial_port.close()
    else:
        time.sleep(1)
        msg = None
        msg = 'power=1200'

    if not msg:
        raise Meter_Exception("meter read timed out")

    # otherwise we get a message with temp and power usage
    m = re.search("power=(\d+)", msg)
    if m is None:
        raise Meter_Exception("couldn't parse msg [%s]" % msg)

    # fake
    temp = 20
    energy = float(m.group(1))

    return temp, energy

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    temp,power = read_meter('/dev/ttyACM0')
    print("%dC %dW" % (temp, power))

