# In the box

* raspberry pi b+
* raspberry pi b
* 2 x usb wifi dongle
* 2 x usb bluetooth dongle
* 2 x usb extender cable
* 2 x sd card (master & slave)
* energy wristband
* pi power supply
* current cost monitor, sender and usb cable, power supply

# Important notes

* this is a beta, so things probably won't work perfectly. With your help we'll
 get the docs and code working better!
* the wristband is not waterproof and probably a bit fragile. Please take care
 of it - there are only 2 in existance.

# Set up

## Energy wristband

charge the energy wristband with a micro usb cable

## master pi

This is the important one that connects to the current cost. Plug in:

* master sd card
* usb wifi
* usb bluetooth on a usb extender cable
* current cost usb cable

The extender cable is used to separate the wifi and bluetooth dongles as they
can cause interferance with each other and reduce the working range of the
system.

Set up the current cost sender, see the section [Fitting the transmitter to your
meter'](http://www.currentcost.com/product-envi-installation.html)

Check you're getting results on the LCD monitor. Connect the usb cable to the
back of the current cost monitor.

Plug in power to the pi.

## Slave pi

Because blue tooth low energy is low range, we use the second pi with the slave
sd card to increase range. Plug in:

* slave sd card
* usb wifi dongle
* usb bluetooth dongle on usb extender cable
* plug in power

# In use

The wristband has only one small button, pressing it will show you the last
energy data on the leds. If the reading is stale (more than 10 minutes) then
the leds will flash on and off.

When a large change in energy happens, the wristband will vibrate and the leds
will show you the change in energy. As you get used to wearing the wristband,
you'll notice the vibration corresponds to an increase or decrease in energy
usage.

## Tweaking

Todo...
