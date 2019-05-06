#!/usr/bin/env python3

import math
from enum import Enum, unique
from typing import List, Optional, Tuple, Dict, Set


# IMPORTANT NOTE: DO NOT IMPORT THE ev3dev.ev3 MODULE IN THIS FILE

@unique
class Direction(Enum):
    """ Directions in degrees """
    NORTH = "N"
    EAST = "E"
    SOUTH = "S"
    WEST = "W"

    def to_int(self):
        if self.value == "N":
            return 1
        elif self.value == "E":
            return 2
        elif self.value == "S":
            return 3
        elif self.value == "W":
            return 4

    def __str__(self):
        return self.value


def to_enum(direction):
    print(direction)
    if direction == "N":
        return Direction.NORTH
    elif direction == "E":
        return Direction.EAST
    elif direction == "S":
        return Direction.SOUTH
    elif direction == "W":
        return Direction.WEST

# simple alias, no magic here
Weight = int
""" 
    Weight of a given path (received from the server)
    value:  -1 if blocked path
            >0 for all other paths
            never 0
"""

@unique
class RelativeDirection(Enum):
    LEFT = 1
    RIGHT = 2
    FORWARD = 3

def find_next_node(node, planet):
    neighbours = planet.get_neighbours(node)
    for n in neighbours:
        if n.has_unexplored_paths():
            return n
        else:
            find_next_node(n, planet)


class Node:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.is_discovered = False  # should be set to True, if discovered
        self.outgoing_paths: Dict[Direction, bool] = dict()
        self.is_visited = False

    def set_found_paths(self, directions: Set[Direction]):
        """
        Set the directions in which paths exist.

        This will also set the node to discovered.

        Args:
            directions: a set of directions in which paths exist
        """
        self.is_discovered = True
        for direction in directions:
            if direction not in self.outgoing_paths:
                self.outgoing_paths[direction] = False

    def set_entry_direction(self, direction):
        """
        Set the entry direction of the node.

        The direction is stored as explored.

        Args:
            direction: the entry direction
        """
        self.outgoing_paths[direction] = True

    def set_path_to_explored(self, direction):
        """
        Set the path in a direction as explored.

        Raises:
            ValueError: if the node does not now the specified direction

        Args:
            direction: the direction that should be set to explored
        """
        if self.is_discovered and direction in self.outgoing_paths:
            self.outgoing_paths[direction] = True
        else:
            raise ValueError(f"No path found in direction {str(direction)}.")

    def get_unexplored_paths(self):
        """
        Get all unexplored path directions

        Returns:
            a set of directions that are not explored
        """
        return {direction for direction, explored in self.outgoing_paths.items() if not explored}

    def has_unexplored_paths(self):
        """
        Check if the node has unexplored paths

        Returns:
            True if the node is undiscovered or not all paths have been explored yet, False otherwise

        """
        if not self.is_discovered:
            return True
        for value in self.outgoing_paths.values():
            if not value:
                return True
        return False

    def as_tuple(self):
        """
        Get the tuple representation of the node

        Returns:
            the coordinates of the node
        """
        return self.x, self.y

    def is_at_point(self, x, y):
        """
        Check if the node is at a point

        Args:
            x: the x coordinate
            y: the y coordinate

        Returns:
            True if the node is at the specified point, False otherwise
        """
        return self.x == x and self.y == y

    def __eq__(self, other):
        return other.x == self.x and other.y == self.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __str__(self):
        return f"({self.x},{self.y}), {self.outgoing_paths}"


class Planet:
    """
    Contains the representation of the map and provides certain functions to manipulate it according to the specifications
    """

    def __init__(self):
        """ Initializes the data structure """
        self.target = None
        self.paths: Set[Tuple[Tuple[Node, Direction], Tuple[Node, Direction], Weight]] = set()
        self.nodes: Set[Node] = set()

    def add_start_node(self, x: int, y: int) -> Node:
        """
        Add the start node

        Args:
            x: x coordinate of start point
            y: y coordinate of start point

        Returns:
            the corresponding node object
        """
        node = Node(x, y)
        self.nodes.add(node)
        self.add_server_path(((x, y), Direction.SOUTH), ((x, y), Direction.SOUTH), -1)
        return node

    def get_unexplored_nodes(self):
        """
        Get all nodes that have or may have unexplored paths

        Returns:
            a set of all unexplored nodes
        """
        return {node for node in self.nodes if node.has_unexplored_paths()}

    def find_node(self, x: int, y: int) -> Optional[Node]:
        """
        Find a node object

        Args:
            x: x coordinate of the node
            y: y coordinate of the node

        Returns:
            the corresponding node or None, if the node does not exist yet
        """
        for node in self.nodes:
            if node.is_at_point(x, y):
                return node
        return None

    def get_neighbours(self, node: Node) -> Set[Node]:
        """
        Get all nodes that are reachable from a node

        Args:
            node: the node, the neighbours should be found to

        Returns:
            a set containing the neighbours of the node
        """
        return {path[1][0] for path in self.paths if path[0][0] == node} - {node}

    def add_server_path(self, start: Tuple[Tuple[int, int], Direction], end: Tuple[Tuple[int, int], Direction],
                        weight: Weight) -> Node:
        """
        Add a path that was sent from the server

        Args:
            start: start point and start direction
            end: end point and end direction
            weight: weight of the path

        Returns:
            the node corresponding to the end point
        """
        end_node = self.__add_path_in_one_direction(start, end, weight)
        self.__add_path_in_one_direction(end, start, weight)
        return end_node

    def __add_path_in_one_direction(self, start: Tuple[Tuple[int, int], Direction],
                                    end: Tuple[Tuple[int, int], Direction],
                                    weight: Weight) -> Node:
        start_node = None
        end_node = None

        for node in self.nodes:
            if node.x == start[0][0] and node.y == start[0][1]:
                start_node = node
            if node.x == end[0][0] and node.y == end[0][1]:
                end_node = node

        if start_node is None:
            start_node = Node(start[0][0], start[0][1])
            self.nodes.add(start_node)
        if end_node is None:
            end_node = Node(end[0][0], end[0][1])
            self.nodes.add(end_node)

        end_node.set_entry_direction(end[1])
        self.paths.add(((start_node, start[1]), (end_node, end[1]), weight))
        return end_node

    def add_path(self, start: Tuple[Tuple[int, int], Direction], target: Tuple[Tuple[int, int], Direction],
                 weight: int):
        """
         Adds a bidirectional path defined between the start and end coordinates to the map and assigns the weight to it
        example:
            add_path(((0, 3), Direction.NORTH), ((0, 3), Direction.WEST), 1)
        :param start: 2-Tuple
        :param target:  2-Tuple
        :param weight: Integer
        :return: void
        """
        self.add_server_path(start, target, weight)
        self.add_server_path(target, start, weight)

    def get_paths(self) -> Dict[Tuple[int, int], Dict[Direction, Tuple[Tuple[int, int], Direction, Weight]]]:
        """
        Returns all paths
        example:
            get_paths() returns:
            {
                (0, 3): {
                    Direction.NORTH: ((0, 3), Direction.WEST, 1),
                    Direction.EAST: ((1, 3), Direction.WEST, 2)
                },
                (1, 3): {
                    Direction.WEST: ((0, 3), Direction.EAST, 2),
                    ...
                },
                ...
            }
        :return: Dict
        """
        path_dict = dict()
        for start, end, weight in self.paths:
            if (start[0].as_tuple()) not in path_dict:
                path_dict[start[0].as_tuple()] = dict()
            path_dict[start[0].as_tuple()][start[1]] = (end[0].as_tuple(), end[1], weight)
        return path_dict

    def shortest_path(self, start: Tuple[int, int], target: Tuple[int, int]) -> Optional[
        List[Tuple[Tuple[int, int], Direction]]]:
        """
        Returns a shortest path between two nodes
        examples:
            shortest_path((0,0), (2,2)) returns: [((0, 0), Direction.EAST), ((1, 0), Direction.NORTH)]
            shortest_path((0,0), (1,2)) returns: None
        :param start: 2-Tuple
        :param target: 2-Tuple
        :return: List, Direction
        """

        paths = self.get_paths()

        if start not in paths.keys() or target not in paths.keys():
            return None

        if start == target:
            return []

        undiscovered_vertices = set(paths.keys())
        distance: Dict[Tuple[int, int], float] = {p: math.inf for p in undiscovered_vertices}
        predecessor: Dict[Tuple[int, int], Tuple[Tuple[int, int], Direction]] = {p: None for p in undiscovered_vertices}

        distance[start] = 0

        while undiscovered_vertices:
            active_point = min(undiscovered_vertices, key=lambda x: distance[x])

            if active_point == target:
                break

            undiscovered_vertices.remove(active_point)

            for (direction, path) in paths[active_point].items():
                if path[2] < 0:
                    continue

                end_point, end_direction = path[0], path[1]

                new_distance = distance[active_point] + path[2]

                if new_distance < distance[end_point]:
                    distance[end_point] = new_distance
                    predecessor[end_point] = active_point, direction

        path = []
        while target != start:
            if target is None or predecessor[target] is None:
                return None

            point, direction = predecessor[target]
            path.insert(0, (point, direction))
            target = point

        return path


if __name__ == '__main__':
    # EXAMPLE:
    planet = Planet()
    start_node = planet.add_start_node(0, 0)
    start_node.set_found_paths({Direction.NORTH, Direction.EAST})
    end_node = planet.add_server_path(((0, 0), Direction.NORTH), ((0, 1), Direction.SOUTH), 1)
    end_node.set_found_paths({Direction.WEST, Direction.NORTH})
    planet.add_server_path(((0, 1), Direction.WEST), ((0, 0), Direction.WEST), 2)
    planet.add_server_path(((0, 0), Direction.EAST), ((1, 0), Direction.WEST), 1)
    planet.add_server_path(((0, 1), Direction.NORTH), ((0, 2), Direction.SOUTH), 1)
    planet.add_server_path(((0, 2), Direction.NORTH), ((0, 3), Direction.SOUTH), 1)
    planet.add_server_path(((0, 2), Direction.EAST), ((2, 2), Direction.WEST), 1)
    planet.add_server_path(((0, 3), Direction.NORTH), ((0, 3), Direction.WEST), 1)
    planet.add_server_path(((0, 3), Direction.EAST), ((2, 2), Direction.NORTH), 1)
    planet.add_server_path(((1, 0), Direction.NORTH), ((2, 2), Direction.SOUTH), 1)
    shortest_path = planet.shortest_path((0, 0), (0, 3))
    print(shortest_path)
