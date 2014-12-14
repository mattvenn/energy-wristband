# RFDuino

* onadvertisement only happens once, not every time
* setinterval works (must have been fixed since this post)
* adc read raises power level and doesn't return without extra effort

# dropout issues

## while working:

meter set to 30ma on regulator input

nothing 4.63,4.76 mA
advert  4.68,4.82 mA

when bust

nothing	4.84
advert  4.88

## lescan

sometimes returns nothing, restarting pi sometimes sorts this.
when broken last, rebooted pi broke connection? Then air could detect it and pi could after reboot. 

Should have tried lescan on pi first.

searching for `hci0 command 0x0406 tx timeout` reveals a bunch of (old) raspi bluetooth issues


hcitool lescan does this when bluetooth broken:
Set scan parameters failed: Input/output error

found this: https://urbanjack.wordpress.com/tag/raspberry-pi/
which explains how to do a reset - which worked. Also slowing usb speed seems a good (crap) solution

tried setting usb bus to slow speed with 

dwc_otg.lpm_enable=0 console=ttyAMA0,115200 kgdboc=ttyAMA0,115200 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline dwc_otg.speed=1 rootwait

on Sun Dec 14 12:41:42 GMT 2014 see what happens
