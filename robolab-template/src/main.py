#!/usr/bin/env python3

import ev3dev.ev3 as ev3
import uuid
import paho.mqtt.client as mqtt
import movement_definitions
import message_content as msc
import communication as communication
import pid
import time
import colourtest
import movement_at_communication_point as abc
import planet as p
from planet import Direction, to_enum, find_next_node
import rotation_controller as rc

client = None  # DO NOT EDIT


"""
========= useful information =========
Unix-password for brick (needed on deploy): g106b19
group-ID: 106
"""

def run():
    # DO NOT EDIT
    # the deploy script uses this variable to stop the mqtt client after your program stops or crashes.
    # your script isn't able to close the client after crashing.
    global client
    client = mqtt.Client(client_id=str(uuid.uuid4()),  # client_id has to be unique among ALL users
                         clean_session=False,
                         protocol=mqtt.MQTTv31)

    # the execution of all code shall be started from within this function
    # ADD YOUR OWN IMPLEMENTATION HEREAFTER
    global messageContent
    messageContent = msc.MessageContent()

    planet = p.Planet()

    comm = communication.Communication(client, messageContent, planet)
    # comm.send_test_planet_message() # testing purpose todo: remove at end

    firstNodeFound = False
    targetReached = False
    mapExplored = False
    lastNode = None
    turnTo = None
    isInShortestPath = False

    while not targetReached or not mapExplored:

        pid.follow_line()
        node = None
        if not firstNodeFound:
            comm.send_deploy_message()
            firstNodeFound = True
            print("Found first node!")
            node = planet.add_start_node(messageContent.getStartX(), messageContent.getStartY())
            print(">First node: ", node)

        else:
            comm.send_path_message()
            #planet.nodes.add(p.Node(messageContent.getStartX(), messageContent.getStartY()))
            print(">Path:", ((lastNode.x, lastNode.y), turnTo), ((messageContent.getEndX(), messageContent.getEndY()), messageContent.getComeFrom()), messageContent.getPathWeight())
            node = planet.add_server_path(((lastNode.x, lastNode.y), turnTo), ((messageContent.getEndX(), messageContent.getEndY()), messageContent.getComeFrom()), messageContent.getPathWeight())
            print(">End node:", node)

        comeFrom = messageContent.getComeFrom()
        if type(comeFrom) != Direction:
            print("come from was no enum yet")
            comeFrom = to_enum(comeFrom)

        # unknown paths are in node after scan
        abc.scan(node, comeFrom)

        if node.has_unexplored_paths():
            turnTo = node.get_unexplored_paths().pop()
        else:
            #turnTo = comeFrom

            for n in planet.nodes:
                if n.has_unexplored_paths() and n.is_visited:
                    print("=====================")
                    print(">Node: ", node, "\nn: ", n)
                    print("=====================")
                    #print(planet.get_paths())
                    #nextNode = find_next_node(node, planet)
                    #print(nextNode)
                    pathlist = planet.shortest_path((node.x, node.y), (n.x, n.y))
                    messageContent.setTargetX(n.x)
                    messageContent.setTargetY(n.y)

                    if pathlist != None:
                        turnTo = pathlist[0][1]

                    print("The pathlist: ", pathlist)
                    print("Turn to next nearest node: ", turnTo)

                else:
                    messageContent.setMessage("Planet" + messageContent.getPlanetName() + " is now discovered property of group 106!")
                    print(messageContent.getMessage())
                    comm.send_exploration_completed_message()
                    mapExplored = True


            # make shortest path, drive this list, continue

        if type(turnTo) != Direction:
            print("turnTo was no enum yet")
            turnTo = to_enum(turnTo)

        messageContent.setStartDirection(turnTo)

        print("We come from: ", comeFrom)
        print("We turn to: ", turnTo)
        print("Node after scan: ", node)
        messageContent.setPathX(node.x)
        messageContent.setPathY(node.y)

        comm.send_path_selection()

        print("Comm sended path selection")
        print("new Start: ", messageContent.getStartDirection())
        print("new End: ", messageContent.getEndDirection())

        turns = rc.rotate_to_target(comeFrom, turnTo)
        if turns < 0:
            movement_definitions.turn_90degree_right()
        else:
            for i in range(0, turns):
                movement_definitions.turn_90degree_left()

        node.set_path_to_explored(turnTo)
        messageContent.setPathStatus("free")

        messageContent.setStartX(messageContent.getEndX())
        messageContent.setStartY(messageContent.getEndY())

        lastNode = node

        #print(node.unknownPaths)

    # when finishing successfully
    ev3.Sound.tone(15000, 1000).wait()


# DO NOT EDIT
if __name__ == '__main__':
    run()
