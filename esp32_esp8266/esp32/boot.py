# This file is executed on every boot (including wake-boot from deepsleep

from machine import reset
from network import WLAN, STA_IF, phy_mode, MODE_11N
from time import ticks_ms
from gc import collect as gc_collect
import ujson as json
from socket import socket as sock, AF_INET, SOCK_DGRAM, IPPROTO_UDP, getaddrinfo

STA_CONF_ARR_PATH = "/sta_conf_arr.json"
PHY_MODE = MODE_11N
STA_TIMEOUT = 5000
AF_INET_BROADCAST = "255.255.255.255"
ADDR_ANNOUNCE_PORT = 1337

def scan_wifi():
    sta_if = WLAN(STA_IF)
    sta_if.active(True)
    scan = sta_if.scan()
    print("\nWiFi Scan:\n\t{:35}, {:14}, {:2}, {:4}, {:4}, {:6}".format("ssid", "bssid", "ch", "rssi", "auth", "hidden"))
    for ssid, bssid, channel, rssi, authmode, hidden in scan:
        print("\t{:35}, 0x{:12}, {:2}, {:4}, {:4}, {:6}".format(ssid, "".join(["{:02x}".format(b) for b in bssid])[:-1], channel, rssi, authmode, hidden))
    print("")
    return scan

def connect_to_ap(ssid, psk):
    sta_if = WLAN(STA_IF)
    sta_if.active(True)
    sta_if.connect(ssid, psk)
    now = ticks_ms()
    while (not sta_if.isconnected()) and ((ticks_ms()-now < STA_TIMEOUT)):
        pass
    if not sta_if.isconnected():
        raise OSError("Could not connect to AP")

def deactivate_sta():
    sta_if = WLAN(STA_IF)
    sta_if.active(True)
    sta_if.connect("", "")
    sta_if.active(False)

def connect_to_wifi():
    sta_conf_arr = json.load(open(STA_CONF_ARR_PATH))
    for ssid, _, _, _, _, _ in scan_wifi():
        for sta_conf in sta_conf_arr:
            if ssid.decode() == sta_conf["ssid"]:
                print("Connecting to "+sta_conf["ssid"])
                try:
                    connect_to_ap(sta_conf["ssid"], sta_conf["psk"])
                except OSError as e:
                    pass
                else:
                    print("Connected to "+sta_conf["ssid"])
                    return
    deactivate_sta()
    raise OSError("No access point available.")

if __name__ == '__main__':
    phy_mode(PHY_MODE)
    try:
        connect_to_wifi()
        s = sock(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
        s.connect((AF_INET_BROADCAST, ADDR_ANNOUNCE_PORT))
        s.send("{}\n".format(WLAN().ifconfig()[0]))
        s.close()
    except KeyError as err:
        print("Key Error: {0}".format(err))
    except OSError as err:
        print("OS Error: {0}".format(err))
    gc.collect()
