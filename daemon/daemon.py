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
data_interval = 60 * 10  # seconds
wristband_timeout = 10
wb = wristband(logging, wristband_timeout)

# set this in the past so wristband is updated when daemon starts
last_data = time.time() - data_interval

# set this flag to True to start with, so that the wristband gets updated
failed_send = True

# set up logging to file - see previous section for more details
log_format = '%(asctime)s %(name)-10s %(levelname)-8s %(message)s'
logging.basicConfig(level=logging.INFO,
                    format=log_format,
                    filename='reader.log')

# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter(log_format)
console.setFormatter(formatter)
# add the handler to the root logger
logger = logging.getLogger('')
logger.addHandler(console)
logger.warning("daemon started")


# main loop
while True:
    try:
        # read meter, might throw an exception
        (temp, power) = read_meter(meter_port, logger, meter_timeout)
        logger.info("meter returned %f W %f C" % (power, temp))

        # update internet service - run as a daemon thread
        xively_t = xively(feed_id, logging, timeout=xively_timeout)
        xively_t.add_datapoint('temperature', temp)
        xively_t.add_datapoint('energy', power)

        # post uptime to help debugging
        f=open("/proc/uptime","r");
        uptime_string=f.readline()
        f.close()
        uptime=uptime_string.split()[0]
        xively_t.add_datapoint('uptime', uptime)

        # get difference in energy
        (last, this) = diff_realtime.diff(power, logging)

        # send to the wristband?
        if last is not None:
            logger.info("sending to wristband")
            # this blocks but times out
            try:
                wb.send(last, this)
            except ValueError as e:
                if e.message == 'timed out':
                    failed_send = True
                    logger.warning("failed to send %d %d, will try later" % (last,this))
                else:
                    raise(e)
            xively_t.add_datapoint('wb-this', this)
        else:
            logger.info("not enough difference")

        # fetch data from wristband?
        if time.time() > last_data + data_interval:
            last_data = time.time()
            (battery, uptime) = wb.get()
            xively_t.add_datapoint('wb-battery', battery)
            xively_t.add_datapoint('wb-uptime', uptime)

            # if the last update failed, try sending it silently
            # (the wristband won't buzz)
            if failed_send == True:
                logger.info("resending %d" % this)
                # this might raise an exception
                wb.re_send(this)
                failed_send = False

        logger.info("start xively thread")
        xively_t.daemon = True
        xively_t.start()

    except ValueError as e:
        logger.error(e)

    # keep a track of running threads
    logger.info("%d threads running", len(threading.enumerate()))
    # in case something goes wrong - prevent rapid looping
    time.sleep(1)
