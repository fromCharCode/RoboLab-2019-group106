import json
# todo: remove in case it is not needed
import planet
from message_content import MessageContent
from planet import to_enum

class Message():

    def __init__(self, msc: MessageContent, planet):
        self.msc = msc
        self.planet = planet
        self.receivedTarget = False

    def write_message(self, dataType):
        print("Writing message...\n<message>")
        data = {}
        data['from'] = 'client'
        data['type'] = dataType

        if dataType == 'ready':
            self.write_ready()
        elif dataType == 'path':
            data['payload'] = {}
            self.write_path(data['payload'])
        elif dataType == 'pathSelect':
            data['payload'] = {}
            self.write_path_select(data['payload'])
        elif dataType == 'targetReached':
            data['payload'] = {}
            self.write_target_reached(data['payload'])
        elif dataType == 'explorationCompleted':
            data['payload'] = {}
            self.write_exploration_completed(data['payload'])
        elif dataType == 'testplanet':
            data['payload'] = {}
            self.write_testplanet(data['payload'])

        data = json.dumps(data, indent=2)
        print(data)
        print("</message>")
        # TODO: remove when test succeed
        return data

    def write_ready(self):
        return

    def write_path(self, payload):
        payload['startX'] = self.msc.getStartX()
        payload['startY'] = self.msc.getStartY()
        payload['startDirection'] = str(self.msc.getStartDirection())
        payload['endX'] = self.msc.getEndX()
        payload['endY'] = self.msc.getEndY()
        payload['endDirection'] = str(self.msc.getEndDirection())
        payload['pathStatus'] = str(self.msc.getPathStatus())
        return payload

    def write_path_select(self, payload):
        payload['startX'] = self.msc.getPathX()
        payload['startY'] = self.msc.getPathY()
        payload['startDirection'] = str(self.msc.getStartDirection())
        return payload

    def write_target_reached(self, payload):
        payload['message'] = self.msc.getMessage()
        return payload

    def write_exploration_completed(self, payload):
        payload['message'] = self.msc.getMessage()
        return payload

    def write_testplanet(self, payload):
        payload['planetName'] = 'Hulk'
        return payload

    # read messages from server and write content to message_content
    def read_message(self, message):
        print('Got message with topic "{}":'.format(message.topic))
        data = json.loads(message.payload.decode('utf-8'))  # get decoded message in utf-8
        print(json.dumps(data, indent=2))  # and convert into JSON; save in variable later
        print("\n")

        self.receivedTarget = False
        type = data['type']


        if type == "planet":
            self.read_planet(data['payload'])
        elif type == "path":
            self.read_path(data['payload'])
        elif type == "pathUnveiled":
            self.read_path_unveiled(data['payload'])
        elif type == "pathSelect":
            self.read_path_select(data['payload'])
        elif type == "target":
            self.read_target(data['payload'])
        elif type == "done":
            self.read_done(data['payload'])
        elif type == "notice":
            self.read_notice(data['payload'])


    # deploy
    def read_planet(self, payload):
        self.msc.setPlanetName(payload['planetName'])
        self.msc.setStartX(payload['startX'])
        self.msc.setStartY(payload['startY'])
        self.msc.setEndX(payload['startX'])
        self.msc.setEndY(payload['startY'])

    def read_path(self, payload):
        self.msc.setStartX(payload['startX'])
        self.msc.setStartY(payload['startY'])
        self.msc.setStartDirection(payload['startDirection'])
        self.msc.setEndX(payload['endX'])
        self.msc.setEndY(payload['endY'])
        self.msc.setEndDirection(payload['endDirection'])
        self.msc.setPathStatus(payload['pathStatus'])
        self.msc.setComeFrom(payload['endDirection'])
        self.msc.setPathWeight(payload['pathWeight'])

    def read_path_unveiled(self, payload):
        self.planet.add_path(
            ((payload['startX'], payload['startY']), to_enum(payload['startDirection'])),
            ((payload['endX'], payload['endY']), to_enum(payload['endDirection'])),
            payload['pathWeight']
        )

    def read_path_select(self, payload):
        self.msc.setStartDirection(payload['startDirection'])

    def read_target(self, payload):
        self.msc.setTargetX(payload['targetX'])
        self.msc.setTargetY(payload['targetY'])
        self.receivedTarget = True
        #planet.shortest_path((self.msc.getStartX, self.msc.getStartY), ()) # todo: call shortest path here

    def read_done(self, payload):
        self.msc.setMessage(payload['message'])

    def read_notice(self, payload):
        self.msc.setMessage(payload['message'])

    def has_target(self):
        return self.receivedTarget