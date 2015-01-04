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

Follow [these instructions to
install](http://stackoverflow.com/questions/24853597/ble-gatttool-cannot-connect-even-though-device-is-discoverable-with-hcitool-lesc)
a newer version.
