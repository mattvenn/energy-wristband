# Programming

The programming port has 4 pins. Pin 1 is marked on the PCB.

* pin 1 - ground
* pin 2 - reset
* pin 3 - rx
* pin 4 - tx

The wristband will need a power supply, so charge the battery or leave it
plugged in via the micro usb charge port.

Use a standard USB/Serial cable for programming (eg FTDI). I've been using 3.3v
version as the system runs on 3v. 

# RFDuino setup

If you are on Windows or Mac, just follow the RFDuino instructions.

## Linux

RFDuino isn't really open source, and so we have to run the programmer binary
using wine.

* Install wine
* Install a recent version of Arduino IDE (>1.5)
* Download and unzip RFDuino library into arduino-1.5.x/hardware/arduino/
* Change RFDLoader to contain this:

    #!/bin/bash
    /usr/bin/wine /home/tomws/arduino-1.5.8/hardware/arduino/RFduino/RFDLoader.exe $1 com1 $3

* You might need to make a symlink from ~/.wine/dosdevices/com1 to /dev/ttyUSB0
* Open Arduino IDE, choose RFDuino for board and /dev/ttyUSB0 for port.
* Good luck!

# Todo

* flash red led on battery low

# Done

* repeat led animation
* PWM control vibration to indicate increasing or decreasing energy
* when last update is too old, flash leds when realtime status requested
