# Battery test

On the 2nd prototype I've left off the potential divider resistors so I can't
measure battery, but power consumption drops from about 20ua to 5ua while
sleeping.

Found that the usb connector isn't soldered properly on the 2nd one ;(

# Road map

* feedback survey - make a survey for my family to fill
* beta test survey - to find most appropriate testers
* promote beta test survey
* instructions - on how to use, range, setup, troubleshooting
* spare kit of stuff in a box
* send off kit
* get results, send feedback survey
* repeat, build a support group of interested people

# UDP repeater - or increasing range

The main issue with the system is that bluetooth low energy just doesn't seem to
have the range. I've tried extending range by [hacking the
aerial](http://www.instructables.com/id/Increase-and-extend-the-range-of-a-USB-Bluetooth-d/),
but it doesn't make much difference. 

After putting the dongle on a usb extension cable at my parents the
range got a lot better. I'm assuming that getting it further away from the wifi
dongle (both at 2.4GHz) reduced interference and improved range.

Strangely, doing the same thing in my (much smaller) flat - it didn't make much
difference.

So how to increase range. Well my laptop is on a fair amount, so while it's on
why not use its bluetooth to pass the message on if the wristband is out of
range from the pi?

If the daemon is started with `--udp_repeat` then it will
broadcast any wristband messages (default 192.168.0.255). 

The [udp repeater](../daemon/udp_repeater.py) program can be started at boot,
and will pass on messages received over UDP to the wristband if it's in range. 

# Docs

Written up an [install and FAQ/problem solving guide](install.md)

# Christmas time tests

After forgetting the energy sender unit of my current cost, I had to write a
[program](http://www.mattvenn.net/2014/12/28/reading-a-geo-minim-energy-meter-with-a-webcam-and-python/) to read my Dad's energy meter with a camera!

With that out of the way I was able to set everything up and try it out on my
family. I've yet to make a quick survey and get them to fill it in.

# Software dev

Been reading up on exception handling - it's been difficult to get the code as
clean as I want it. Some good info here:

* http://nedbatchelder.com/text/exceptions-vs-status.html
* https://docs.python.org/2/tutorial/errors.html
* http://stackoverflow.com/questions/2901000/the-correct-way-to-define-an-exception-in-python-without-pylint-complaining

# Usage notes

* Not too big
* Button is too small to press easily
* UI additions:
    * vibrate change speed up or down to indicate increase or decrease in energy
    * show lights as animation for longer or repeat a few times
    * show low battery as a flashing red led
* Worth thinking about BLE range extension or just give up on BLE?

## More usage notes from Sun Dec 28 15:49:47 GMT 2014

* putting blue tooth dongle on a usb extension lead made a big difference to
 range
* couple of big battery voltage drops - don't know why
* alerts seem to be useful and appropriate

# PCB assembly notes

Very exciting to have a working wristband on! Assembled today and reflowed a
double sided board for the first time. 

* bottom stencil needs flipping in eagle or inkscape before cutting
* charge LED was wrong way round - fixed on v2 schematic
* battery monitor potential divider needs more thought. High impedance is better
 for low energy usage, but is a big mismatch in ADC input. Better to have low
 impedance and switch with a fet. Set R2 to 76k in software to compensate.
* didn't have the resistors for divider on hand, so used 226k and 100k.
* this combination should use about 13uA. Module uses 4uA. I see a total of 23uA
 so something else has changed - check LDO quiescent.
* tested PWM mosfet control of motor - works, will add to code
* removed R7 (motor resister) as not needed with VCC = 2.8V
* got too excited and removed a board too fast from oven - then dropped it!
* tried to remove a RFDuino module from the breakout board and screwed it.
 Should have used the oven!

# Software update

Daemonized python software and all done much better with proper timeouts and
exception handling.

[See code here](./daemon/)

# RFDuino issues and learnings

* not open source really, should have researched tool chain properly.
* onadvertisement() only happens once, not every time
* setinterval works (must have been fixed since this post)
* adc read raises power level and doesn't return without extra effort

# Bluetooth research

found a [great BLE resource here](http://www.eetimes.com/document.asp?doc_id=1278927)

# Bluetooth dropout issues

Annoyingly, the bluetooth seems flakey on the Pi. I think it is another boring
USB issue. The music ADC breaks at the same time and a reboot always fixes both.

## hcitool lescan

Sometimes returns nothing, restarting pi sometimes sorts this.
when broken last, rebooted pi broke connection? Then mac air could detect it and pi could after reboot. 

Searching for `hci0 command 0x0406 tx timeout` reveals a bunch of (old) raspi
bluetooth issues.

hcitool lescan does this when bluetooth broken:

    Set scan parameters failed: Input/output error

Funny how it locks the device so another computer can't see it or talk to it.

## Sun Dec 14 12:41:42 GMT 2014

Found this: https://urbanjack.wordpress.com/tag/raspberry-pi/
which explains how to do a reset - which worked. Also slowing usb speed seems a good (crap) solution

tried setting usb bus to slow speed with 

dwc_otg.lpm_enable=0 console=ttyAMA0,115200 kgdboc=ttyAMA0,115200 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline dwc_otg.speed=1 rootwait

## Sun Dec 14 16:41:07 GMT 2014

Slow usb bus speed broke audio playing. Set it back to how it was before and swapped the pihub hub for a pluggable one.

## Sun Dec 21 09:45:51 GMT 2014

Was working, then started music which didn't work. Then hcitool lescan failed.
So probably a usb contention issue with the Pi. Will check this with a simpler
setup. My home pi has about 8 USB devices attached.

# PCBs designed

Ordered from OSHpark. Paid extra for fast delivery.

* order placed 26/11
* back from fab 8/12
* sent 9/12
* delivered 16/12

# components for PCB chosen and ordered

See the [google drive doc](https://docs.google.com/spreadsheets/d/1oj70GuA22dZxQOM_nt-e6gl6c6SbQOTN_fw_uVvux9A/edit?usp=sharing) for component choice and calculations.

The main extra components used are:

* Used the MCP73831T LiPo charger - the same one that was in the sparkfun
 charger I'm using to test. Requires only 3 external components.
* Using the TPS78228DDCT LDO regulator to 2.8v. I thought I might go switched
 mode for efficiency, but actually as the circuit is mostly sleeping and using
 4uA, an LDO is more efficient - but only if it has a low quiescent current.
 This model is just 1uA!
* 110mAH LiPo - calculated to give months of usage - wait to see the reality!
 Hopefully we can downsize this in the future.

# Software 

Python script working on raspberry pi communicates to wristband when energy
changes by a large enough amount.

Energy usage is from a current cost meter.

[Graphs and feeds are here](https://xively.com/feeds/130883)

# working breadboarded prototype

with RFduino, LEDs and motor.

RFduino draws 4uA in deep sleep.

