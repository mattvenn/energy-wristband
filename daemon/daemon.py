#!/usr/bin/env python
import threading
import time
import logging

from meter import read_meter
from wristband import wristband
import diff_realtime
from xively import xively

# for xively
feed_id = "130883"
xively_timeout = 10

# meter
meter_port = "/dev/ttyUSB0"
meter_timeout = 10

# wrist band
wristband_timeout = 6
data_interval = 60 * 10  # seconds

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

# main loop
last_data = time.time()
wb = wristband(logging, wristband_timeout)
while True:
    try:
        # read meter, might throw an exception
        (temp, power) = read_meter(meter_port, logger, meter_timeout)
        logger.info("meter returned %f W %f C" % (power, temp))

        # update internet service - run as a daemon thread
        xively_t = xively(feed_id, logging, timeout=xively_timeout)
        xively_t.add_datapoint('temperature', temp)
        xively_t.add_datapoint('energy', power)

        # get difference in energy
        (last, this) = diff_realtime.diff(power, logging)

        # send to the wristband?
        if last is not None:
            logger.info("sending to wristband")
            # this blocks but times out
            wb.send(last, this)
            xively_t.add_datapoint('wb-this', this)
        else:
            logger.info("not enough difference")

        # fetch data from wristband?
        if time.time() > last_data + data_interval:
            last_data = time.time()
            (battery, uptime) = wb.get()
            xively_t.add_datapoint('wb-battery', battery)
            xively_t.add_datapoint('wb-uptime', uptime)

        logger.info("start xively thread")
        xively_t.daemon = True
        xively_t.start()

    except ValueError as e:
        logger.error(e)

    # keep a track of running threads
    logger.info("%d threads running", len(threading.enumerate()))
    # in case something goes wrong - prevent rapid looping
    time.sleep(1)
