from math import cos, pi

TAU = 2*pi

HUE_MAX = 720
SAT_MIN = 0
SAT_MAX = 100
BRI_MIN = 0
BRI_MAX = 100

def hsb_curve_sin(angle):
    while angle < 0:
        angle += TAU
    while angle >= TAU:
        angle -= TAU
    return (1-cos(3*angle/2))/2 if angle < 2*TAU/3 else 0

def hsb2rgb(hue_sat_bri):
    hue, sat, bri = hue_sat_bri
    hue %= HUE_MAX
    angle = TAU*hue/HUE_MAX
    sat = max(min(sat, SAT_MAX), SAT_MIN)
    bri = max(min(bri, BRI_MAX), BRI_MIN)

    red =   int(255*hsb_curve_sin(angle+TAU/3))
    green = int(255*hsb_curve_sin(angle))
    blue =  int(255*hsb_curve_sin(angle-TAU/3))

    result = [red, green, blue]

    for i in range(0, len(result)):
        result[i] *= sat/SAT_MAX
        result[i] += 255*(SAT_MAX-sat)/SAT_MAX
        result[i] *= bri/BRI_MAX
        result[i] = int(result[i])

    return result
