import serial
import time
import re

serial_debug = False

"""
see current cost XML format doc here:
http://www.currentcost.com/cc128/xml.htm
"""

def read_meter(meter_port, logger, timeout=10):
    if not serial_debug:
        serial_port = serial.Serial()
        serial_port.port = meter_port
        serial_port.baudrate = 57600
        serial_port.timeout = timeout
        serial_port.open()
        serial_port.flushInput()

        # this times out
        logger.debug("opened serial with %ds timeout" % serial_port.timeout)
        msg = serial_port.readline()
        serial_port.close()
    else:
        time.sleep(1)
        msg = None
        msg = '<msg><src>CC128-v0.11</src><dsb>00591</dsb><time>03:01:16</time><tmpr>15.7</tmpr><sensor>0</sensor><id>00077</id><type>1</type><ch1><watts>02777</watts></ch1></msg>'
        msg = 'msg =<msg><src>CC128-v0.11</src><dsb>01424</dsb><time>09:04:10</time><hist><dsw>01425</dsw><type>1</type><units>kwhr</units><data><sensor>0</sensor><h594>0.179</h594><h592>0.319</h592><h590>0.383</h590><h588>0.220</h588></data><data><sensor>1</sensor><h594>0.000</h594><h592>0.000</h592><h590>0.000</h590><h588>0.000</h588></data><data><sensor>2</sensor><h594>0.000</h594><h592>0.000</h592><h590>0.000</h590><h588>0.000</h588></data><data><sensor>3</sensor><h594>0.000</h594><h592>0.000</h592><h590>0.000</h590><h588>0.000</h588></data><data><sensor>4</sensor><h594>0.000</h594><h592>0.000</h592><h590>0.000</h590><h588>0.000</h588></data><data><sensor>5</sensor><h594>0.000</h594><h592>0.000</h592><h590>0.000</h590><h588>0.000</h588></data><data><sensor>6</sensor><h594>0.000</h594><h592>0.000</h592><h590>0.000</h590><h588>0.000</h588></data><data><sensor>7</sensor><h594>0.000</h594><h592>0.000</h592><h590>0.000</h590><h588>0.000</h588></data><data><sensor>8</sensor><h594>0.000</h594><h592>0.000</h592><h590>0.000</h590><h588>0.000</h588></data><data><sensor>9</sensor><h594>0.000</h594><h592>0.000</h592><h590>0.000</h590><h588>0.000</h588></data></hist></msg>'

    if not msg:
        raise ValueError("meter read timed out")

    # could be a history message (on every odd hour)
    m = re.search("</?hist>", msg)
    if m is not None:
        raise ValueError("ignoring history message")

    # otherwise we get a message with temp and power usage
    m = re.search("<tmpr>(\d+\.\d+)</tmpr>.*<watts>(\d+)</watts>", msg)
    if m is None:
        raise ValueError("couldn't parse msg [%s]" % msg)

    return float(m.group(1)), float(m.group(2))
