from network import WLAN, STA_IF, phy_mode, MODE_11N, STAT_CONNECTING, STAT_GOT_IP
import ujson as json

STA_CONF_ARR_PATH = "/wifi_tk/sta_conf_arr.json"
PHY_MODE = MODE_11N

sta_if = WLAN(STA_IF)

def deactivate():
    sta_if.active(True)
    sta_if.connect("", "")
    sta_if.active(False)

def _connect_to_ap(ssid, psk):
    phy_mode(PHY_MODE)
    sta_if = WLAN(STA_IF)
    sta_if.active(True)
    sta_if.connect(ssid, psk)
    while sta_if.status() == STAT_CONNECTING:
        pass
    if sta_if.status() != STAT_GOT_IP:
        raise OSError("Could not connect.")

def scan_wifi():
    phy_mode(PHY_MODE)
    sta_if.active(True)
    scan = sta_if.scan()
    print("\nWiFi Scan:\n\t{:35}, {:14}, {:2}, {:4}, {:4}, {:6}".format("ssid", "bssid", "ch", "rssi", "auth", "hidden"))
    for ssid, bssid, channel, rssi, authmode, hidden in scan:
        print("\t{:35}, 0x{:12}, {:2}, {:4}, {:4}, {:6}".format(ssid, "".join(["{:02x}".format(b) for b in bssid])[:-1], channel, rssi, authmode, hidden))
    print("")
    return scan

def add_ap(ssid, psk):
    sta_conf_arr = list()
    tuple = {"ssid": ssid, "psk": psk}
    try:
        with open(STA_CONF_ARR_PATH, "r") as sta_conf_arr_file:
            sta_conf_arr = json.load(sta_conf_arr_file)
    except:
        print("Didn't find %s. Creating file." % STA_CONF_ARR_PATH)
    if not tuple in sta_conf_arr:
        sta_conf_arr += [tuple]
    print(sta_conf_arr)
    with open(STA_CONF_ARR_PATH, "w") as sta_conf_arr_file:
        json.dump(sta_conf_arr, sta_conf_arr_file)


def connect_to_wifi():
    sta_conf_arr = json.load(open(STA_CONF_ARR_PATH))
    for ssid, _, _, _, _, _ in scan_wifi():
        for sta_conf in sta_conf_arr:
            if ssid.decode() == sta_conf["ssid"]:
                print("Connecting to "+sta_conf["ssid"])
                try:
                    _connect_to_ap(sta_conf["ssid"], sta_conf["psk"])
                except OSError as e:
                    pass
                else:
                    print("Connected to "+sta_conf["ssid"])
                    return
    deactivate()
    raise OSError("No known access point available.")
