# This file is executed on every boot (including wake-boot from deepsleep)
import gc
import webrepl
import ujson as json
from wifi_tk import sta, ap
from machine import reset
from socket import socket as sock, AF_INET, SOCK_DGRAM, getaddrinfo
import ssid_psk_query

ADDR_ANNOUNCE_PORT = 1337

def get_broadcast_addr():
    ifconf = sta.sta_if.ifconfig()
    addr_arr = [int(char) for char in ifconf[0].split('.')]
    inv_mask_arr = [int(char)^255 for char in ifconf[1].split('.')]
    return '.'.join([str(pair[0] | pair[1]) for pair in zip(addr_arr, inv_mask_arr)])

if __name__ == "__main__":
    webrepl.start()
    gc.collect()
    while not sta.sta_if.isconnected():
        try:
            sta.connect_to_wifi()
            s = sock(AF_INET, SOCK_DGRAM)
            s.connect((get_broadcast_addr(), ADDR_ANNOUNCE_PORT))
            s.send("\n".join(sta.sta_if.ifconfig())+"\n"*2)
            s.close()
        except KeyError as err:
            print("Key Error: {0}".format(err))
        except OSError as err:
            print("OS Error: {0}".format(err))
            print("Starting AP")
            ap.start()
            ssid, psk = ssid_psk_query.query()
            sta.add_ap(ssid, psk)
