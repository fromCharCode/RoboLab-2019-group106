import ev3dev.ev3 as ev3
import time

mr = ev3.LargeMotor('outB')  # right motor
ml = ev3.LargeMotor('outC')  # left motor
cs = ev3.ColorSensor('in3')  # colour sensor


def move_forward():
    mr.run_direct(duty_cycle_sp=100)
    ml.run_direct(duty_cycle_sp=100)


def move_backward():
    mr.run_direct(duty_cycle_sp=-100)
    ml.run_direct(duty_cycle_sp=-100)


def turn_right():
    mr.run_direct(duty_cycle_sp=-100)
    ml.run_direct(duty_cycle_sp=100)


def turn_left():
    mr.run_direct(duty_cycle_sp=100)
    ml.run_direct(duty_cycle_sp=-100)


def stop():
    mr.stop()
    ml.stop()

def turn_around():
    mr.run_to_rel_pos(speed_sp=300, position_sp=310)
    ml.run_to_rel_pos(speed_sp=-300, position_sp=-310)
    mr.wait_while('running')
    ml.wait_while('running')

def turn_90degree_right():
    mr.run_to_rel_pos(speed_sp=300, position_sp=130)
    ml.run_to_rel_pos(speed_sp=-300, position_sp=-130)
    mr.wait_while('running')
    ml.wait_while('running')


def find_line_right():
    lv = cs.bin_data("hhh")
    grey = (lv[0] + lv[1] + lv[2]) / 3

    if grey > 130:
        mr.run_to_rel_pos(speed_sp=300, position_sp=-100)
        ml.run_to_rel_pos(speed_sp=300, position_sp=+100)
        mr.wait_while('running')
        ml.wait_while('running')
        return True
    else:
        return False


def find_line_left():
    lv = cs.bin_data("hhh")
    grey = (lv[0] + lv[1] + lv[2]) / 3

    #if grey > 130:
    mr.run_to_rel_pos(speed_sp=300, position_sp=-50)
    ml.run_to_rel_pos(speed_sp=300, position_sp=50)
    mr.wait_while('running')
    ml.wait_while('running')
    return True
    #else:
     #   return False


def turn_90degree_left():
    mr.run_to_rel_pos(speed_sp=-300, position_sp=-165)
    ml.run_to_rel_pos(speed_sp=300, position_sp=+165)
    mr.wait_while('running')
    ml.wait_while('running')
    find_line_left()

def turn_360degree():                       #to the left
    mr.run_to_rel_pos(speed_sp=-200, position_sp=-695)
    ml.run_to_rel_pos(speed_sp=200, position_sp=+695)


def is_running():
    if (
        mr.is_running
    ):
        return True
    elif(
        ml.is_running
    ):
        return True
    else:
        return False

