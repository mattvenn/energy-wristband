#!/usr/bin/env python
import threading
import time
import logging
import argparse

from meter import read_meter, Meter_Exception
#from meter_photo import read_meter, Meter_Exception
from wristband import wristband, WB_Exception
import diff
from xively import xively


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="read meter, post to internet and send to energy wristband")
    
    #parser.add_argument('--fetch-data', action='store_true', help="fetch data for specific machine")

    parser.add_argument('--max_energy', action='store', type=int,
        help="max energy", default=3000)
    parser.add_argument('--max_time', action='store', type=int,
        help="max time before disregarding energy", default=30)
    parser.add_argument('--sens', action='store', type=int,
        help="sensitivity of differentiation in W/s", default=50)
    parser.add_argument('-d','--debug',
        help='print lots of debugging statements',
        action="store_const", dest="loglevel", const=logging.DEBUG,
        default=logging.WARNING)
    parser.add_argument('-v','--verbose',
        help='be verbose',
        action="store_const", dest="loglevel", const=logging.INFO)
    parser.add_argument('--meter_port', help="current cost meter port",
        default="/dev/ttyUSB0")
    parser.add_argument('--meter_timeout', type=int, help="meter timeout",
        default=10)

    args = parser.parse_args()

    # for xively
    feed_id = "130883"
    xively_timeout = 10

    # wrist band
    data_interval = 60 * 10  # seconds
    wristband_timeout = 10
    wb = wristband(logging, wristband_timeout)

    # get diff object
    diff = diff.diff_energy(logging, max_energy=args.max_energy,
        sens=args.sens,
        max_time=args.max_time)    

    # set this in the past so wristband is updated when daemon starts
    last_data = time.time() - data_interval

    # set up logging to file - see previous section for more details
    log_format = '%(asctime)s %(name)-10s %(levelname)-8s %(message)s'
    logging.basicConfig(level=args.loglevel,
                        format=log_format,
                        filename='reader.log')


    # main loop
    logging.warning("daemon started")
    while True:
        try:
            # read meter, might raise an exception
            (temp, energy) = read_meter(args.meter_port, logging, args.meter_timeout)
            time.sleep(5)
            logging.info("meter returned %dW %.1fC" % (energy, temp))

            # update internet service - run as a daemon thread
            xively_t = xively(feed_id, logging, timeout=xively_timeout, uptime=True)
            xively_t.daemon = True  # could this be done in the class?
            xively_t.add_datapoint('temperature', temp)
            xively_t.add_datapoint('energy', energy)

            # get last good energy point
            last_energy = diff.get_last_valid(energy)

            # convert the real energies to divisions from 1 to 4
            energy_div = diff.energy_to_div(energy)
            last_energy_div = diff.energy_to_div(last_energy)

            # send/receive to the wristband? can raise exceptions
            try:
                # need to send?
                if energy_div != last_energy_div:
                    xively_t.add_datapoint('wb-this', energy_div)
                    # this blocks but times out
                    wb.send(last_energy_div, energy_div)

                # need to fetch data from wristband?
                if time.time() > last_data + data_interval:
                    last_data = time.time()
                    (battery, uptime) = wb.get()
                    xively_t.add_datapoint('wb-battery', battery)
                    xively_t.add_datapoint('wb-uptime', uptime)

                    # resend the last energy value in case a previous send failed
                    logging.info("resending last energy %d" % energy_div)
                    wb.re_send(energy_div)

            except WB_Exception as e:
                logging.warning(e)

            logging.info("send data to xively")
            xively_t.start()
        except Meter_Exception as e:
            logging.info(e)
            # prevent rapid looping
            time.sleep(1)
        except KeyboardInterrupt as e:
            logging.warning("caught interrupt - quitting")
            break
        # keep a track of running threads
        logging.debug("%d threads running", len(threading.enumerate()))
