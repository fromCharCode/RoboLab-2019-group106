from planet import Direction

class Path:
    def __init__(self, direction):
        self.direction = direction


class RevealedPath(Path):
    pass


class UnknownPath(Path):
    pass


class Node:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbours = []
        self.status = 'undiscovered'     #should turn into discovered
        self.knownPaths = []
        self.unknownPaths = []

    def add_neighbour(self, v):
        if v not in self.neighbours:
            self.neighbours.append(v)

    def add_unknownpath(self, direction):
        if direction not in self.unknownPaths:
            self.unknownPaths.append(direction)

    def add_knownpath(self, lastNode, startDir, endNode, endDir, weight):
        # path: {startNode, endNode, sDir, eDir, weight=-1}

            self.knownPaths.append() # todo: remind: this is not just direction

    def get_unknownpaths(self):
        return self.unknownPaths

    def get_knownpath(self):
        return self.knownPaths


class Map:

    nodes = []
    paths = []

    def __init__(self):
        self.nodes = []
        self.paths = []

    def add_node(self, node):
        if node not in self.nodes:
            self.nodes.append(node)

    def get_nodes(self):
        return self.nodes
'''
    def add_path(self, startNode, startDirection, endX, endY, endDirection, weight=-1):
        if (
                #a in self.nodes
                #and b in self.nodes
        ):
            # for a.add_neighbour(b)
            #    b.add_neighbour(a)

            return True
        else:
            return False

        startNode.addKnownPath()
'''