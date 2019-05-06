#!/usr/bin/env python3

import time
import message_handler

class Communication:
    """
        Class to hold the MQTT client
        Feel free to add functions, change the constructor and the example send_message() to satisfy your requirements and thereby solve the task according to the specifications
    """

    hasFinished = False
    isSent = False
    isReceived = False

    def __init__(self, mqtt_client, message_content, planet):
        """ Initializes communication module, connect to server, subscribe, etc. """
        # THESE TWO VARIABLES MUST NOT BE CHANGED
        self.client = mqtt_client

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_subscribe = self.on_subscribe
        # self.client.on_unsubscribe = self.on_unsubscribe # <- never needed
        self.client.on_publish = self.on_publish  # maybe remove, useful for debugging json files
        self.client.on_message = self.on_message_excepthandler
        self.client.on_log = self.on_log  # debugging
        self.planet = planet


        # ADD YOUR VARIABLES HERE
        # == VARIABLES FOR CONNECTION ==
        self.broker = 'mothership.inf.tu-dresden.de'
        #self.broker = 'iot.eclipse.org' # external broker for testing purpose only! TODO: remove at end
        self.group = '106'
        self.password = 'f2uNNL68OY'
        self.port = 8883
        self.qos = 1 # Quality of Service 1 is required by project -> message will be send at least one times
        self.topic = 'explorer/'

        # implementing message content. this got initialized in main.py: run(); we use the same reference here
        self.message_content = message_content
        self.msh = message_handler.Message(message_content, planet) # message content now in message handler to store received values and send stored

        # self.run_connection() # NOTE: could be useful for connections on node.

    def run_connection(self, dataType):
        self.client.username_pw_set(self.group, password=self.password)
        self.client.connect(self.broker, port=self.port)
        self.client.subscribe(self.topic+self.group, qos=self.qos)
        # TODO: activate on deployment

        # self.client.connect(self.broker) # chose this one for testing, commend lines above

        self.client.loop_start()

        # Start listening to incoming messages
        # todo: while isNotFinished
        while True:
            # send or receive
            time.sleep(2)

            if not self.isSent:
                # send message # todo: give into this method what shall be send. call send_message from in here
                self.client.publish(self.topic + self.group, self.msh.write_message(dataType=dataType), qos=self.qos,
                                    retain=False)
                time.sleep(1) # security
                self.isSent = True

            if self.isReceived:
                break

            print("in connection loop")

        # TODO: break condition is the flag isSent. maybe change- is also important for receiving

        # End listening to incoming messages
        self.client.loop_stop()
        self.client.disconnect()


    # START OF CALLBACKS
    def on_connect(self, client, data, flags, rc):

        # handle the RC, output
        if rc == 0:
            print("Successfully connected")
        else:
            errorMessage = ""
            if rc == 1:
                errorMessage = "incorrect protocol version"
            elif rc == 2:
                errorMessage = "invalid client identifier"
            elif rc == 3:
                errorMessage = "server unavailable"
            elif rc == 4:
                errorMessage = "bad username or password"
            elif rc == 5:
                errorMessage = "not authorized"

            print(f'Connection refused - {errorMessage}')

        # subscribe to broker
        # client.subscribe(self.topic+self.group)

        # publish first message

        #client.publish(self.topic+self.group, self.msh.write_message(dataType='testplanet'), qos=self.qos, retain=False)


    def on_disconnect(self, client, data, rc):
        if (rc != 0):
            print("Unexpected disconnect - Code: "+str(rc))


    def on_subscribe(self, client, data, mid, granted_qos):
        # qos should always be 1
        pass


    def on_publish(self, client, data, mid):
        print('Publishing message...')


    # THIS FUNCTIONS SIGNATURE MUST NOT BE CHANGED
    def on_message(self, client, data, message):
        #print('Got message with topic "{}":'.format(message.topic))
        #data = json.loads(message.payload.decode('utf-8')) # get decoded message in utf-8
        #print(json.dumps(data, indent=2)) # and convert into JSON; save in variable later
        #print("\n")
        self.msh.read_message(message)
        self.isReceived = True

    # this is a helper method that catches errors and prints them
    # it is necessary because on_message is called by paho-mqtt in a different thread and exceptions
    # are not handled in that thread
    #
    # you don't need to change this method at all
    def on_message_excepthandler(self, client, data, message):
        try:
            self.on_message(client, data, message)
        except:
            import traceback
            traceback.print_exc()
            raise


    def on_log(self, client, data, level, buf):
        print("log: " + buf)
    # END OF CALLBACKS


# abstract method for sending messages
    def send_message(self, dataType):
        """ Sends given message to specified channel """
        # TODO: ensure that connection is running
        self.isSent = False
        self.run_connection(dataType)


# the important methods for sending different kinds of messages
    def send_deploy_message(self):
        self.set_topic('explorer/')
        self.send_message('ready')
        self.set_topic('planet/'+self.message_content.getPlanetName()+"-")
        self.client.subscribe(self.topic+self.group)

    def send_path_message(self):
        self.set_topic('planet/'+self.message_content.getPlanetName()+"-")
        self.send_message('path')

    def send_path_selection(self):
        self.set_topic('planet/'+self.message_content.getPlanetName()+"-")
        self.send_message('pathSelect')

    def send_target_reached_message(self):
        self.set_topic('explorer/')
        self.send_message('targetReached')

    def send_exploration_completed_message(self):
        self.set_topic('explorer/')
        self.send_message('explorationCompleted')

    def send_test_planet_message(self):
        self.set_topic('explorer/')
        self.send_message('testplanet')

# set topic
    def set_topic(self, topic):
        self.topic = topic