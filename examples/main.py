from machine import Pin
from esp import neopixel_write
from time import sleep_us
from hsb import hsb2rgb, HUE_MAX

SAT = 100
BRI = 5
DELAY_US = 100000
NUM_LEDS = 64
PIN_LEDS = 12

grb_list = [hsb2rgb([(HUE_MAX*i)//NUM_LEDS, SAT, BRI]) for i in range(0, NUM_LEDS)]
flat_grb_list = [item for sublist in grb_list for item in sublist]
grb_buf = bytearray(flat_grb_list)


# if __name__ == '__main__':
#     hue = 0
#     print("Starting Test loop")
#     print("Ctrl+C to get prompt")
GPIO_LED = Pin(PIN_LEDS, Pin.OUT)
while True:
    neopixel_write(GPIO_LED, grb_buf, True)
    grb_buf = grb_buf[3:] + grb_buf[:3]
    sleep_us(DELAY_US)
