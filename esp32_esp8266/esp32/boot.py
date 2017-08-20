# This file is executed on every boot (including wake-boot from deepsleep

from machine import reset
from machine import Pin
from machine import TouchPad
import network
from time import ticks_ms
from gc import collect as gc_collect
import ujson as json

STA_CONF_PATH = "/sta_conf.json"
STA_TIMEOUT = 5000

def connect_to_wifi():
    sta_conf = json.loads(open(STA_CONF_PATH).read())
    network.phy_mode(network.MODE_11G)
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(sta_conf["ssid"], sta_conf["pass"])
    now = ticks_ms()
    while (not sta_if.isconnected()) and ((ticks_ms()-now < STA_TIMEOUT)):
        pass
    if not sta_if.isconnected():
        raise OSError("Could not connect to AP")

if __name__ == "__main__":
    try:
        connect_to_wifi()
    except KeyError as err:
        print("Key Error: {0}".format(err))
    except OSError as err:
        print("OS Error: {0}".format(err))
    gc_collect()
