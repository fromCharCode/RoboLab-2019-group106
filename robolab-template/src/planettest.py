#!/usr/bin/env python3

import unittest
from planet import Direction, Planet


class ExampleTestPlanet(unittest.TestCase):
    def setUp(self):
        """
        Instantiates the planet data structure and fills it with paths
        example planet:

        +--+
        |  |
        +-0,3------+
           |       |
          0,2-----2,2 (target)
           |      /
        +-0,1    /
        |  |    /
        +-0,0-1,0
           |
        (start)

        """

        # set your data structure
        self.planet = Planet()

        # add the paths
        self.planet.add_path(((0, 0), Direction.NORTH), ((0, 1), Direction.SOUTH), 1)
        self.planet.add_path(((0, 1), Direction.WEST), ((0, 0), Direction.WEST), 1)

    def test_target_not_reachable_with_loop(self):
        # does the shortest path algorithm loop infinitely?
        # there is no shortest path
        self.assertIsNone(self.planet.shortest_path((0, 0), (1, 2)))


class YourFirstTestPlanet(unittest.TestCase):
    def setUp(self):
        """
        Instantiates the planet data structure and fills it with paths

        MODEL YOUR TEST PLANET HERE (if you'd like):

        """
        # set your data structure
        self.planet = Planet()

        # ADD YOUR PATHS HERE:
        self.planet.add_path(((0, 0), Direction.NORTH), ((0, 1), Direction.SOUTH))
        self.planet.add_path(((0, 0), Direction.EAST), ((0, 1), Direction.EAST))
        self.planet.add_path(((0, 1), Direction.NORTH), ((1, 2), Direction.WEST))
        self.planet.add_path(((1, 2), Direction.SOUTH), ((1, 1), Direction.NORTH))
        self.planet.add_path(((1, 1), Direction.EAST), ((2, 1), Direction.WEST))
        self.planet.add_path(((1, 1), Direction.SOUTH), ((2, 0), Direction.WEST))
        self.planet.add_path(((2, 1), Direction.NORTH), ((2, 2), Direction.SOUTH))
        self.planet.add_path(((2, 2), Direction.NORTH), ((2, 2), Direction.WEST))
        self.planet.add_path(((2, 0), Direction.NORTH), ((2, 1), Direction.SOUTH))
        self.planet.add_path(((2, 0), Direction.EAST), ((4, 0), Direction.WEST))
        self.planet.add_path(((4, 0), Direction.NORTH), ((4, 1), Direction.SOUTH))
        self.planet.add_path(((4, 0), Direction.EAST), ((4, 1), Direction.EAST))

        # todo: implement hulk as tesplanet for testing stuff.

    def test_integrity(self):
        # were all paths added correctly to the planet
        # check if add_path() works by using get_paths()
        self.fail('implement me!')

    def test_empty_planet(self):
        self.fail('implement me!')

    def test_target_not_reachable(self):
        self.fail('implement me!')

    def test_shortest_path(self):
        # at least 2 possible paths
        # self.assertEqual()
        # self.failUnlessEqual
        self.fail('implement me!')

    def test_same_length(self):
        # at least 2 possible paths with the same weight
        self.fail('implement me!')

    def test_shortest_path_with_loop(self):
        # does the shortest path algorithm loop infinitely?
        # there is a shortest path
        self.fail('implement me!')

    def test_target_not_reachable_with_loop(self):
        # there is no shortest path
        self.fail('implement me!')


class TestHulk(unittest.TestCase):
    def setUp(self):
        """
        Instantiates the planet data structure and fills it with paths

        MODEL YOUR TEST PLANET HERE (if you'd like):

        """
        # set your data structure
        self.planet = Planet()
        self.planet.add_path(((13, 37), Direction.NORTH), ((13, 38), Direction.SOUTH), 1)
        self.planet.add_path(((13, 38), Direction.NORTH), ((14, 39), Direction.WEST), 1)
        self.planet.add_path(((14, 39), Direction.SOUTH), ((14, 38), Direction.NORTH), 1)
        self.planet.add_path(((14, 38), Direction.SOUTH), ((15, 37), Direction.WEST), 1)
        self.planet.add_path(((15, 37), Direction.NORTH), ((15, 38), Direction.SOUTH), 1)
        self.planet.add_path(((15, 38), Direction.WEST), ((14, 38), Direction.EAST), 1)
        self.planet.add_path(((17, 37), Direction.SOUTH), ((17, 37), Direction.EAST), -1)
        print(self.planet.shortest_path((14, 38), (17, 37)))


    def test_shortest_path(self):
        print()


if __name__ == "__main__":
    unittest.main()
