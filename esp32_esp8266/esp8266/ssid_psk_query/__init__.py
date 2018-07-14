from socket import getaddrinfo, socket
from ure import compile

RE_GET = compile("GET")
RE_SSID = compile("SSID=.*&")
RE_PSK = compile("PSK=.* ")

HTML_PATH = "/ssid_psk_query/ssid_psk_form.html"

def _unescape(urlstring):
    urlstring = urlstring.replace("+", " ")
    return urlstring

def query():
    addr = getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket()
    s.bind(addr)
    s.listen(1)
    print('listening on ', addr)
    ssid = None
    psk = None
    while ssid == None or psk == None:
        cl, addr = s.accept()
        print('client connected from', addr)
        cl_file = cl.makefile('rwb', 0)
        while True:
            line = cl_file.readline()
            string = line.decode()
            if RE_GET.match(string):
                ssid_match = RE_SSID.search(string)
                psk_match = RE_PSK.search(string)
                if ssid_match != None and psk_match != None:
                    ssid = _unescape(ssid_match.group(0)[5:-1])
                    psk = _unescape(psk_match.group(0)[4:-1])
            if not line or line == b'\r\n':
                break
        with open(HTML_PATH) as html_f:
            cl.send(html_f.read())
        cl.close()
    s.close()
    return ssid, psk
