# Install

This doc explains how the software was put together to create the images.
It is intended for my reference and for people who want to build their own setups.

# Raspberry Pi

Assuming installing from a fresh raspbian.
Sun Jan  4 14:20:48 GMT 2015

## Python dependancies and Repo

On the command line:

    sudo apt-get install python-setuptools
    sudo easy_install pip
    git clone http://github.com/mattvenn/energy-wristband
    cd energy-wristband/daemon/
    pip install -r requirements.txt

## Bluetooth

bluez for raspbian is old and doesn't support bluetooth low energy (BLE) very
well. 

Follow [these instructions to install](http://www.elinux.org/RPi_Bluetooth_LE) a
newer version.

Then copy gatttool to /usr/bin:

    sudo cp attrib/gatttool /usr/bin/

And reboot:

    sudo reboot

## Test connection

Find BLE address of the wristband:

    sudo hcitool lescan

If all's working then you'll be returned an address for a device called 'e-wb'.
If you have problems, see the section below.

Then try testing the wristband module (replace XX for your address):

    cd energy-wristband/daemon/
    ./wristband.py --address XX:XX:XX:XX:XX:XX

The wristband should vibrate and lights flash.

## Xively

If you want to do internet logging, you'll need to setup xively - which starts
by requesting a developer account and waiting ;(. Sorry I didn't realise it was
closed to the public now.

After you've got an account, create a feed and make a note of the id. Then make
a file in the daemon directory called xively.key with an api key that has access to
write to the feed.

Configure the daemon process by using the --xively_feed argument with your feed
id.

## Start the daemon

Run the daemon like this:

    ./daemon.py --debug --wb_address XX:XX:XX:XX:XX:XX

The daemon runs silently, so check daemon.log for lots of debugging information.
When things are running ok, you can remove --debug or replace it with --verbose
as you wish.

Other important options are:

* --meter_port - which port the current cost meter port is on
* --max_energy - max energy your home uses (what 4 leds on the wristband means)
* --sens - how sensitive the system is to change in Watts per second

## Automatically start the daemon at boot

Edit crontab:

    crontab -e

I've found bluetooth + raspberry pi + usb to be unreliable, and these extra
lines have helped:

    #give a kick after boot
    @reboot sudo hciconfig hci0 down; sudo hciconfig hci0 up

    #every hour restart device
    0 * * * * sudo hciconfig hci0 down; sudo hciconfig hci0 up

    #start the e-wb daemon
    @reboot cd ~/energy-wristband/daemon/ ; ./daemon.py -v --ble_address E7:2C:35:BC:D2:B9 --xively_feed 130883 --udp_repeat

## Problems

### Battery

Check the wristband battery is charged.

### Bluetooth

If you have problems detecting the wristband then it might be to do with an
older version of bluez. Check the link above about installing a newer version.

### 'Set scan parameters failed: File descriptor in bad state'

    sudo hcitool hci0 down
    sudo hcitool hci0 up

If this works then you can put the commands above in your crontab or
/etc/rc.local so it gets done at boot (see section above on crontab)

### problematic bluetooth adapters

It could also be an incompatible bluetooth dongle. I had issues with Asus BT400
(marked as OK on the [raspberry pi
wiki](http://elinux.org/RPi_USB_Bluetooth_adapters)).

[This worked for
me](http://urbanjack.wordpress.com/2014/02/26/bluetooth-low-energy-ble-on-raspberry-pi-with-asus-bt-400/)

