# This file is executed on every boot (including wake-boot from deepsleep)
import gc
import network
import webrepl

STA_CONF_PATH = "/sta_conf.json"

def connect_to_wifi():
    sta_conf = json.loads(open(STA_CONF_PATH).read())
    network.phy_mode(network.MODE_11N)
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(sta_conf["ssid"], sta_conf["pass"])
    while network.STAT_CONNECTING == sta_if.status():
        pass
    if network.STAT_GOT_IP != sta_if.status():
        print("Could not connect to WiFi")
        raise OSError

if __name__ == '__main__':
    webrepl.start()
    try:
        connect_to_wifi()
    except KeyError as err:
        print("Key Error: {0}".format(err))
    except OSError as err:
        print("OS Error: {0}".format(err))
    gc.collect()
