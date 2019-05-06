from planet import Direction, to_enum

class MessageContent():
    def __init__(self):
        self.planetName = ""
        self.startX = 0
        self.startY = 0
        self.startDirection = str(Direction.SOUTH)
        self.endX = 0
        self.endY = 0
        self.endDirection = str(Direction.EAST)
        self.targetX = 0
        self.targetY = 0
        self.pathStatus = "free"
        self.pathWeight = -1
        self.message = ""
        self.debug = ""
        self.comeFrom = str(Direction.SOUTH)
        self.pathX = 0
        self.pathY = 0

# setters
    def setPlanetName(self, planetName):
        self.planetName = planetName
    
    def setStartX(self, startX):
        self.startX = int(startX)
    
    def setStartY(self, startY):
        self.startY = int(startY)
    
    def setStartDirection(self, startDirection):
        self.startDirection = str(startDirection)
    
    def setEndX(self, endX):
        self.endX = int(endX)
    
    def setEndY(self, endY):
        self.endY = int(endY)
    
    def setEndDirection(self, endDirection):
        self.endDirection = str(endDirection)
    
    def setTargetX(self, targetX):
        self.targetX = int(targetX)
    
    def setTargetY(self, targetY):
        self.targetY = int(targetY)
    
    def setPathStatus(self, pathStatus):
        self.pathStatus = pathStatus
    
    def setPathWeight(self, pathWeight):
        self.pathWeight = int(pathWeight)
    
    def setMessage(self, message):
        self.message = message
    
    def setDebug(self, debug):
        self.debug = debug

    def setComeFrom(self, comeFrom):
        self.comeFrom = comeFrom

    def setPathX(self, pathX):
        self.pathX = pathX

    def setPathY(self, pathY):
        self.pathY = pathY

# getters
    def getPlanetName(self):
        return self.planetName
    
    def getStartX(self):
        return self.startX
    
    def getStartY(self):
        return self.startY
    
    def getStartDirection(self):
        return to_enum(self.startDirection)
    
    def getEndX(self):
        return self.endX
    
    def getEndY(self):
        return self.endY
    
    def getEndDirection(self):
        return to_enum(self.endDirection)
    
    def getTargetX(self):
        return self.targetX
    
    def getTargetY(self):
        return self.targetY
    
    def getPathStatus(self):
        return self.pathStatus
    
    def getPathWeight(self):
        return self.pathWeight
    
    def getMessage(self):
        return self.message

    def getDebug(self):
        return self.debug

    def getComeFrom(self):
        return to_enum(self.comeFrom)

    def getPathX(self):
        return self.pathX

    def getPathY(self):
        return self.pathY
