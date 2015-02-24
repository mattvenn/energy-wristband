# Todo

* use something different to xively - xively doesn't give easy free access
 anymore
    * thingspeak?
* plugins for meter and monitoring?

# Done

* config file? - yes PLEASE! - slightly hacky - could be improved
* udp repeater stuff in progress
    * needs to be added to firmware so wristband can ignore duplicates
* command line options
* change diff() method name to get_last() or something more meaningful
* diff object borken because as history moves on the differential is repeated
* diff_realtime was originally written for use on the command line. Perhaps
 convert to object and do history storage internally rather than file system?
* diff_realtime is broken now because it will return a diff if its just 100w
 over the limit
* work out if power or energy is correct term and use that only - it's ENERGY!
 in WATTS!
* poll gatttool, don't wait the full 10 seconds
* catch ctrl-C
* update wb with current energy at beginning or if it reboots
* only post once per minute for xively - decided to leave as is
* fetch battery life and uptime from wristband, post to xively
    * if fails, wait for a bit before trying again
* need to maintain a small queue of bluetooth and xively threads, joining later?
    * xively threads don't need limiting because they will time out after 30s
* what happens if thread throws exception, will parent catch it - still need to
  join
    * unhandled exception will kill thread but not affect parent
    * daemon threads don't need joining
* deal with histroy from cc:
