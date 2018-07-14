from network import WLAN, AP_IF, phy_mode, MODE_11N, AUTH_OPEN, AUTH_WEP, AUTH_WPA_PSK, AUTH_WPA2_PSK, AUTH_WPA_WPA2_PSK
import ujson as json

AP_CONFIG_PATH = "/wifi_tk/ap_config.json"
AP_PASSWORD_PATH = "/wifi_tk/ap_password"
PHY_MODE = MODE_11N

ap_if = WLAN(AP_IF)

def _save_config():
    config = {
        "essid": ap_if.config("essid"),
        "authmode": ap_if.config("authmode"),
        "ifconfig": ap_if.ifconfig()
    }
    with open(AP_CONFIG_PATH, "w+") as ap_config_f:
        json.dump(config, ap_config_f)

def set_ifconfig(ip_address, netmask, gateway, dns):
    active = ap_if.active()
    ap_if.active(True)
    ap_if.ifconfig((ip_address, netmask, gateway, dns))
    ap_if.active(active)
    _save_config()

def set_config(essid, authmode, password):
    active = ap_if.active()
    ap_if.active(True)
    ap_if.config(essid="ESP8266", authmode=authmode, password=password)
    ap_if.active(active)
    with open(AP_PASSWORD_PATH, "w+") as ap_password_f:
        ap_password_f.write(password)
    _save_config()

def start():
    ap_if.active(True)
    phy_mode(PHY_MODE)
    config = dict()
    password = ""
    with open(AP_CONFIG_PATH) as ap_config_f:
        config = json.load(ap_config_f)
    with open(AP_PASSWORD_PATH) as ap_password_f:
        password = ap_password_f.read()
    ap_if.config(essid=config["essid"], authmode=config["authmode"], password="%s" % password)
    ap_if.ifconfig(config["ifconfig"])
