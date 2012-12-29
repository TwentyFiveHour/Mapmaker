__author__ = 'Aaron Kaufman'
import basicmap
import roadbuilder
import unittest as test
import perlin_noise
import math


#Python unit test for roadbuilder.py!



class TestRoadBuilder(test.TestCase):

    def setUp(self):
        self.seq = range(10)

    def test_complex_a_star_validity(self):

        #now:  We need to test our A* algorithm on a more complex route, requiring routing around obstacles.
        map = basicmap.TileMap(10,10)
        map.clearMap('water')
        map.getTile(0,0).terrain = 'grass'
        map.getTile(0,1).terrain = 'grass'
        map.getTile(0,2).terrain = 'grass'
        map.getTile(0,3).terrain = 'grass'
        map.getTile(0,4).terrain = 'grass'
        map.getTile(1,4).terrain = 'grass'
        map.getTile(2,4).terrain = 'grass'
        map.getTile(3,4).terrain = 'grass'
        map.getTile(4,4).terrain = 'grass'
        map.getTile(5,4).terrain = 'grass'
        map.getTile(5,3).terrain = 'grass'
        map.getTile(5,2).terrain = 'grass'
        map.getTile(5,1).terrain = 'grass'
        map.getTile(5,0).terrain = 'grass'
        A2 = map.getTile(5,0)
        B2 = map.getTile(0,0)
        A2.city = "A"
        B2.city = "B"
        astar2 = roadbuilder.AStarNodeMap(map, A2, B2)
        result2 = astar2.getAStarResult()
        self.assertTrue(map.getTile(4,4) in result2)
        self.assertTrue(len(result2) ==14)
        invalid_tiles = [tile for tile in result2 if tile.terrain == 'water']
        self.assertTrue(len(invalid_tiles) == 0)



    def test_a_star_correctness(self):
        map = basicmap.TileMap(7,7)
        map.clearMap('water')
        map.getTile(0,0).terrain = 'grass'
        map.getTile(0,1).terrain = 'grass'
        map.getTile(0,2).terrain = 'grass'
        map.getTile(1,2).terrain = 'grass'
        map.getTile(2,2).terrain = 'grass'
        map.getTile(3,2).terrain = 'grass'
        map.getTile(4,2).terrain = 'grass'
        #below should not get traversed (this is the long way around)
        map.getTile(0,3).terrain = 'grass'
        map.getTile(0,4).terrain = 'grass'
        map.getTile(1,4).terrain = 'grass'
        map.getTile(2,4).terrain = 'grass'
        map.getTile(3,4).terrain = 'grass'
        map.getTile(4,4).terrain = 'grass'
        map.getTile(5,4).terrain = 'grass'
        map.getTile(5,3).terrain = 'grass'
        #above should not be traversed
        map.getTile(5,2).terrain = 'grass'
        map.getTile(5,1).terrain = 'grass'
        map.getTile(5,0).terrain = 'grass'


        A2 = map.getTile(5,0)
        B2 = map.getTile(0,0)
        A2.city = "A"
        B2.city = "B"
        astar2 = roadbuilder.AStarNodeMap(map, A2, B2)
        result2 = astar2.getAStarResult()
        self.assertTrue(map.getTile(4,4) not in result2)
        self.assertTrue(map.getTile(5,2) in result2, [tile.x.__str__() + ", " + tile.y.__str__() for tile in result2])
        self.assertTrue(map.getTile(3,2) in result2)
        self.assertTrue(len(result2) ==10)
        invalid_tiles = [tile for tile in result2 if tile.terrain == 'water']
        self.assertTrue(len(invalid_tiles) == 0)

    def test_simple_a_star(self):
        #Now, a test of the AStarNodeMap in the most basic case.

        map = basicmap.TileMap(10,10)
        map.clearMap('water')
        map.getTile(0,0).terrain = 'grass'
        map.getTile(0,1).terrain = 'grass'
        map.getTile(0,2).terrain = 'grass'

        A = map.getTile(0,2)
        B = map.getTile(0,0)
        A.city = "A"
        B.city = "B"

        map.getTile(2,2).terrain = 'grass'
        map.getTile(2,2).city = "C"


        astar = roadbuilder.AStarNodeMap(map, A, B)
        result = astar.getAStarResult()
        self.assertTrue(result[0] == B)
        self.assertTrue(result[1].terrain == 'grass')
        self.assertTrue(result[2] == A)

    def test_contiguous_city_tiles(self):
        #FIRST:  Contiguous city tile test.
        #Question asked: Does our algorithm properly determine what cities are connectable in the most basic case?

        map = basicmap.TileMap(4,4)
        map.clearMap('water')
        map.getTile(0,0).terrain = 'grass'
        map.getTile(0,1).terrain = 'grass'
        map.getTile(0,2).terrain = 'grass'

        A = map.getTile(0,2)
        B = map.getTile(0,0)
        A.city = "A"
        B.city = "B"

        map.getTile(2,2).terrain = 'grass'
        map.getTile(2,2).city = "C"

        lis = roadbuilder.findJoinableCitySets(map)
        num_groups = 0
        while (lis):
            cur = lis.pop()
            if (len(cur) == 2):  #There needs to be one list of length two containing A and B.
                t = cur.pop()
                num_groups+=1
                self.assertTrue(t.city == 'A' or t.city == 'B')
            elif (len(cur) == 1):
                t = cur.pop()
                self.assertTrue(t.city == 'C')
                num_groups+=1



class TestPerlinNoiseGeneration(test.TestCase):
    def test_perlin_noise(self):
        gen = perlin_noise.perlinNoiseGenerator()
        a = gen.noise2d(2,3)
        b = gen.noise2d(2,3)

        c = gen.noise2d(3,2)
        self.assertTrue(a==b)
        self.assertTrue(a!=c)

        gen2 = perlin_noise.perlinNoiseGenerator()
        self.assertTrue(gen2.noise2d(3,3) != gen.noise2d(3,3))
        point = 1,1.4

        this_one = gen.interpolate(*point)
        that_one = gen.interpolate(*point)

        a_different_one = gen.interpolate(30,8.3)
        self.assertTrue(this_one == that_one)
        self.assertTrue(this_one != a_different_one)

        a_mid_point = 30.5,30.5
        x,y=a_mid_point
        a = math.floor(x),math.floor(y)
        b = math.floor(x),math.ceil(y)
        c = math.ceil(x), math.floor(y)
        d = math.ceil(x), math.ceil(y)

        outer_points = a,b,c,d
        noise = [gen.noise2d(x,y) for x,y in outer_points]
        average = sum(noise)/float(len(noise))
        calculated = gen.interpolate(30.5,30.5)
        #Algorithm requires that a point midway between all nearest vertices have a height equal to that
        #of all points.
        self.assertTrue(math.fabs(average - calculated) < 0.001)

        rounded_point = 30,30
        #Checks that the noise generated for that point is the same as the interpolated value for that point.
        self.assertTrue(gen.interpolate(*rounded_point) == gen.noise2d(*rounded_point))

