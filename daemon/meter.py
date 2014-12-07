import serial
import time
import re

serial_debug = True


def read_meter(meter_port, timeout=10):
    if not serial_debug:
        serial_port = serial.Serial()
        serial_port.port = meter_port
        serial_port.baudrate = 57600
        serial_port.timeout = timeout
        serial_port.open()
        serial_port.flushInput()

        # this times out
        logger.info("opened serial with %ds timeout" % serial_port.timeout)
        msg = serial_port.readline()
        serial_port.close()
    else:
        time.sleep(1)
        msg = None
        msg = '<msg><src>CC128-v0.11</src><dsb>00591</dsb><time>03:01:16</time><tmpr>15.7</tmpr><sensor>0</sensor><id>00077</id><type>1</type><ch1><watts>02777</watts></ch1></msg>'

    if not msg:
        raise ValueError("meter read timed out")

    m = re.search("<tmpr>(\d+\.\d+)</tmpr>.*<watts>(\d+)</watts>", msg)

    if m is None:
        raise ValueError("couldn't parse msg [%s]" % msg)

    return float(m.group(1)), float(m.group(2))
