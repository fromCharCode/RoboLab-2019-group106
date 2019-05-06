import ev3dev.ev3 as ev3
import time
cs = ev3.ColorSensor()
cs.mode = 'RGB-RAW'
def getcolour_rgb():
    print(cs.bin_data("hhh"))
    time.sleep(5)

#black (30,60,21)
#white (239,416,200)
#red (156,62,23)
#blue (40,161,102)

