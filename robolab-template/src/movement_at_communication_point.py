import ev3dev.ev3 as ev3
import pid
import time
import movement_definitions as m
#from planet import Node
from planet import Direction, RelativeDirection, Node

mr = ev3.LargeMotor('outB')  # right motor
ml = ev3.LargeMotor('outC')  # left motor
cs = ev3.ColorSensor('in3')  # colour sensor


#def blue_point():
    #30 < lv[0] < 50
    #150 < lv[1] < 170
    #90 < lv[2] < 110

#def red_point():
    #145 < lv[0] < 165
    #50 < lv[1] < 70
    #12 < lv[2] < 32


def find_points():
    lv = cs.bin_data("hhh")
    if (                                #blue point
        20 < lv[0] < 60
        and(140 < lv[1] < 180)
        and(80 < lv[2] < 120)
    ):
        return True
    elif(                               #red point
        130 < lv[0] < 175
        and(40 < lv[1] < 80)
        and(5 < lv[2] < 40)
    ):
        return True
    else:
        return False


def stop_at_points():
    if find_points():
        mr.stop()
        ml.stop()
        return True
    return False


def drive_behind_point():
    if find_points():
        mr.run_to_rel_pos(speed_sp=40, position_sp=160)
        ml.run_to_rel_pos(speed_sp=40, position_sp=140)
        mr.wait_while('running')
        ml.wait_while('running')
        return True
    return False


def cal_directions(relative_direction: RelativeDirection, entry_direction: Direction):
    if (entry_direction == Direction.NORTH):
        if relative_direction == RelativeDirection.RIGHT:
            return Direction.WEST
        if relative_direction == RelativeDirection.LEFT:
            return Direction.EAST
        if relative_direction == RelativeDirection.FORWARD:
            return Direction.SOUTH
    elif(entry_direction == Direction.EAST):
        if relative_direction == RelativeDirection.RIGHT:
            return Direction.NORTH
        if relative_direction == RelativeDirection.LEFT:
            return Direction.SOUTH
        if relative_direction == RelativeDirection.FORWARD:
            return Direction.WEST
    elif (entry_direction == Direction.SOUTH):
        if relative_direction == RelativeDirection.RIGHT:
            return Direction.EAST
        if relative_direction == RelativeDirection.LEFT:
            return Direction.WEST
        if relative_direction == RelativeDirection.FORWARD:
            return Direction.NORTH
    elif (entry_direction == Direction.WEST):
        if relative_direction == RelativeDirection.RIGHT:
            return Direction.SOUTH
        if relative_direction == RelativeDirection.LEFT:
            return Direction.NORTH
        if relative_direction == RelativeDirection.FORWARD:
            return Direction.EAST


def scan(node : Node, entry_direction : Direction):
    drive_behind_point()
    a = ml.position
    foundPaths = set()

    m.turn_360degree()


    print("--- start scan")

    while m.is_running():
        lv = cs.bin_data("hhh")
        grey = (lv[0] + lv[1] + lv[2]) / 3

        if(
            grey < 170
        ):
            b = ml.position
            if (
                60 < b-a < 250
            ):
                absolute_direction = cal_directions(RelativeDirection.LEFT, entry_direction)
                foundPaths.add(absolute_direction)
            elif(
                480 < b-a < 560
            ):
                absolute_direction = cal_directions(RelativeDirection.RIGHT, entry_direction)
                foundPaths.add(absolute_direction)
            elif(
                650 < b-a < 715
            ):
                absolute_direction = cal_directions(RelativeDirection.FORWARD, entry_direction)
                foundPaths.add(absolute_direction)

    print("--- finished scan")
    node.set_found_paths(foundPaths)
    node.is_visited = True

    for fp in foundPaths:
        print("found path: ", str(fp))

    mr.wait_while('running')
    ml.wait_while('running')