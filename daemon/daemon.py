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
        try:
            # read meter, might throw an exception
            (temp, energy) = read_meter(meter_port, logger, meter_timeout)
        except ValueError as e:
            logger.info(e)
            # prevent rapid looping
            time.sleep(1)
        else:
            logger.info("meter returned %fW %fC" % (energy, temp))
            energy_div = diff_realtime.energy_to_div(energy)

            # update internet service - run as a daemon thread
            xively_t = xively(feed_id, logging, timeout=xively_timeout)
            xively_t.add_datapoint('temperature', temp)
            xively_t.add_datapoint('energy', energy)

            # post uptime to help debugging
            f=open("/proc/uptime","r");
            uptime_string=f.readline()
            f.close()
            uptime=uptime_string.split()[0]
            xively_t.add_datapoint('uptime', uptime)

            # get difference in energy
            try:
                last_energy_div = diff_realtime.diff(energy_div, logging)
                # send to the wristband?
                if energy_div != last_energy_div:
                    # this blocks but times out
                    wb.send(last_energy_div, energy_div)
                    xively_t.add_datapoint('wb-this', energy_div)
            except ValueError as e:
                logger.debug(e)

            # time to fetch data from wristband?
            if time.time() > last_data + data_interval:
                last_data = time.time()
                (battery, uptime) = wb.get()
                xively_t.add_datapoint('wb-battery', battery)
                xively_t.add_datapoint('wb-uptime', uptime)

                # resend the last energy value in case a previous send failed
                logger.info("resending last energy %d" % energy_div)
                wb.re_send(energy_div)

            logger.info("send data to xively")
            xively_t.daemon = True
            xively_t.start()

        # keep a track of running threads
        logger.debug("%d threads running", len(threading.enumerate()))

    except KeyboardInterrupt as e:
        logger.warning("caught interrupt - quitting")
        break


