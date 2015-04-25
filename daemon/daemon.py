#!/usr/bin/env python
import threading
import time
import logging
import argparse

#from meter import read_meter, Meter_Exception
#from meter_photo import read_meter, Meter_Exception
from meter_arduino import read_meter, Meter_Exception

from wristband import wristband, WB_Exception
import diff
from xively import xively, Xively_Exception

def setup_logs():
    log_format = logging.Formatter('%(asctime)s - %(name)-12s - %(levelname)-8s - %(message)s')
    # configure the client logging
    log = logging.getLogger('')
    # has to be set to debug as is the root logger
    log.setLevel(logging.DEBUG)


    # create console handler and set level to info
    ch = logging.StreamHandler()
    ch.setLevel(args.loglevel)

    # create formatter for console
    ch.setFormatter(log_format)
    log.addHandler(ch)

    # create file handler and set to debug
    fh = logging.FileHandler('daemon.log')
    fh.setLevel(args.loglevel)

    fh.setFormatter(log_format)
    log.addHandler(fh)

    if args.loglevel == logging.DEBUG:
        from logging_tree import printout
        printout()
    return log

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="read meter, post to internet and send to energy wristband")
    
    from ConfigParser import ConfigParser, NoSectionError
    config = ConfigParser()
    config.read('config.rc')
    d_ble_address = config.get('ble', 'address')
    d_ble_timeout = config.getint('ble', 'timeout')
    d_max_energy = config.getint('energy', 'max_energy')
    d_max_time = config.getint('energy', 'max_time')
    d_sens = config.getint('energy', 'sensitivity')
    d_udp_repeat = config.getboolean('daemon', 'udp_repeat')

    parser.add_argument('--udp_repeat', action='store_const', const=True,
        default=d_udp_repeat,
        help="increase coverage by broadcasting via UDP to other computers")
    parser.add_argument('--max_energy', action='store', type=int,
        help="max energy", default=d_max_energy)
    parser.add_argument('--max_time', action='store', type=int,
        help="max time before disregarding energy", default=d_max_time)
    parser.add_argument('--sens', action='store', type=int,
        help="sensitivity of differentiation in W/s", default=d_sens)
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
    parser.add_argument('--ble_address', help="BLE address of wristband",
        default = d_ble_address)
    parser.add_argument('--wristband_timeout', action='store', type=int, 
        help="timeout for gatttool", default=d_ble_timeout)
    parser.add_argument('--xively_feed', help="id of your xively feed",
        default = None)

    args = parser.parse_args()

    # set up logging
    log = setup_logs()

    xively_timeout = 10

    # wrist band
    data_interval = 60 * 10  # seconds
    wb = wristband(args.ble_address, 
            args.wristband_timeout,
            udp_repeat=args.udp_repeat)

    # get diff object
    diff = diff.diff_energy(max_energy=args.max_energy,
        sens=args.sens,
        max_time=args.max_time)    

    # set this in the past so wristband is updated when daemon starts
    last_data = time.time() - data_interval


    # startup messages
    log.warning("daemon started")
    log.warning("max energy=%dW, sens=%dW/s" % (args.max_energy,args.sens))
    log.warning("BLE address=%s timeout=%d" % (args.ble_address, args.wristband_timeout))
    if args.xively_feed is not None:
        log.warning("xively feed id=%s" % args.xively_feed)
    else:
        log.warning("not sending to xively")
    if args.udp_repeat:
        log.warning("using udp to increase coverage")
    else:
        log.warning("not using udp")


    # main loop
    while True:
        try:
            # read meter, might raise an exception
            (temp, energy) = read_meter(args.meter_port, args.meter_timeout)
            time.sleep(5)
            log.info("meter returned %dW %.1fC" % (energy, temp))

            # update internet service - run as a daemon thread
            if args.xively_feed is not None:
                xively_t = xively(args.xively_feed, timeout=xively_timeout, uptime=True)
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
                    if args.xively_feed is not None:
                        xively_t.add_datapoint('wb-this', energy_div)
                    # this blocks but times out
                    wb.send(last_energy_div, energy_div)

                # need to fetch/update wristband?
                if time.time() > last_data + data_interval:
                    last_data = time.time()

                    # resend last energy value in case previous send failed
                    log.info("resending last energy %d" % energy_div)
                    wb.re_send(energy_div)

                    # fetch data
                    (battery, uptime) = wb.get()
                    if args.xively_feed is not None:
                        xively_t.add_datapoint('wb-battery', battery)
                        xively_t.add_datapoint('wb-uptime', uptime)

            except WB_Exception as e:
                log.warning(e)

            if args.xively_feed is not None:
                log.info("send data to xively")
                xively_t.start()
        except Meter_Exception as e:
            log.info(e)
            # prevent rapid looping
            time.sleep(1)
        except KeyboardInterrupt as e:
            log.warning("caught interrupt - quitting")
            break
        except Xively_Exception as e:
            log.error(e)
            break 
        except Exception as e: # catch all
            log.error("unexpected error!")
            log.error(e)
            break
        # keep a track of running threads
        log.debug("%d threads running", len(threading.enumerate()))
