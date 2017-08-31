# ESP8266 and ESP32
These files are scripts and config template to be used for micropython running
on the ESP32 or EPS8266 802.11 enabled micro controllers.

## Station Mode Config Array
The `sta_conf_arr.json` holds an array of dictionaries which contain the SSID
and PSK of access points. The `boot.py` for both controllers scans for APs, then
iterates through the array and tries to connect.

**TL:DR** : Put your WiFi credentials in the `sta_conf_arr.json`.

## Useful Links
* [ampy](https://github.com/adafruit/ampy) for file manipulation in the ESP
