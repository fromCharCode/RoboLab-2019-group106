import ev3dev.ev3 as ev3
import time
import movement_at_communication_point as move
import movement_definitions
from map import Map

mr = ev3.LargeMotor('outB')  # right motor
ml = ev3.LargeMotor('outC')  # left motor
us = ev3.UltrasonicSensor ('in2')
cs = ev3.ColorSensor('in3')  # colour sensor
cs.mode = 'RGB-RAW'
#gs = ev3.GyroSensor('in2')
#gs.mode = 'GYRO-Rate'
#gs.mode = 'GYRO-ANG'


value_black = 37    #(30,60,21)
value_white = 285   #(239,416,200)
offset = (value_black + value_white)/2       #161


def follow_line():
    blocked = False
    kp = 14             #12,1,25,30
    ki = 1.2
    kd = 25
    tp = 35
    integral = 0
    lasterror = 0
    while True:
        distance = us.distance_centimeters
        if distance <= 7:
            blocked = True
            mr.stop()
            ml.stop()
            movement_definitions.turn_around()

        lv = cs.bin_data("hhh")
        grey = (lv[0] + lv[1] + lv[2])/3
        error = (grey - offset)/100
        integral = (1/3)*integral + error
        d = error - lasterror
        turn = (kp * error) + (ki * integral) + (kd * d)

        mr.run_direct(duty_cycle_sp=tp + turn)
        ml.run_direct(duty_cycle_sp=tp - turn)

        lasterror = error
        if move.drive_behind_point():
            time.sleep(.5)
            break
    print("blocked", blocked)

