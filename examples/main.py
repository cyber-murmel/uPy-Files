from machine import Pin, TouchPad
from neopixel import NeoPixel
from time import sleep_us
from hsb import hsb2rgb, HUE_MAX

TOUCH_THRESH = 1000
SAT = 100
BRI = 15
HUE_STEP = 1
DELAY_US = 0

np = NeoPixel(Pin(2), 1)
tp = TouchPad(Pin(33))

np[0] = [0, 0, 0]
np.write()

if __name__ == '__main__':
    hue = 0
    print("Starting Test loop")
    print("Ctrl+C to get prompt")
    while True:
        if tp.read() < TOUCH_THRESH:
            hue += HUE_STEP
            hue %= HUE_MAX
            np[0] = hsb2rgb([hue, SAT, BRI]);
            np.write()
            sleep_us(DELAY_US)

