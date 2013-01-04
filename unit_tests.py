__author__ = 'Aaron Kaufman'
import world_map
import graph_tools
import unittest as test
import perlin_noise
import math
import utils


#Python unit test for graph_tools.py!
world_map.POLAR_BIAS = 0
world_map.ISLAND_BIAS = 0 #Don't want them interfering with my measurements.

class test_world_wrap(test.TestCase):
    def test_perlin_noise_wrap(self):
        gen = perlin_noise.perlinNoiseGenerator()
        gen.wrap_x = 3
        gen.wrap_y = 3
        self.assertTrue(gen.noise2d(1,0)==gen.noise2d(1,3))
        self.assertAlmostEqual(gen.interpolate(1,0), gen.interpolate(1,3))
        self.assertAlmostEqual(gen.interpolate(1.5,0), gen.interpolate(1.5,3))

    def test_perlin_noise_on_map(self):
        map = world_map.TileMap(80,10)
        gen = map.buildPerlinNoiseGenerator(10)
        for x in range(0,10):
            print(gen.noise2d(x,0))
        self.assertEqual(gen.noise2d(7,0), gen.noise2d(0,0))
        halfway = gen.interpolate(6.5,0)
        should_be_halfway = .5 * (gen.interpolate(7,0) + gen.interpolate(0,0))
        self.assertAlmostEqual(halfway, should_be_halfway)

    def test_map_gen(self):
        map = world_map.TileMap(80,20)
        map.wrap_x = True
        map.wrap_y = True
        map.smoothness = 10
        map.remake()
        self.assertTrue(isPrettyClose(map.getTile(79,0).height, map.getTile(0,0).height),
            "got these values for height: " + str(map.getTile(79,0).height) + "  " +str(map.getTile(0,0).height))
        i = 0
        max_tries=20
        while(isPrettyClose(map.getTile(35,0).height, map.getTile(0,0).height) and i < max_tries):
            map.remake()
            self.assertTrue(isPrettyClose(map.getTile(79,0).height, map.getTile(0,0).height),
                "got these values for height: " + str(map.getTile(79,0).height) + "  " +str(map.getTile(0,0).height))
            i+=1

        if (i==max_tries):
            #This suggests we keep getting values in the middle identical to those at the ends, rendering
            #our test invalid.
            self.fail()
        self.assertFalse(isPrettyClose(map.getTile(40,0).height, map.getTile(0,0).height))


class test_road_builder(test.TestCase):


    def test_complex_a_star_validity(self):

        #now:  We need to test our A* algorithm on a more complex route, requiring routing around obstacles.
        map = world_map.TileMap(10,10)
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
        astar2 = world_map._AStarNodeMap(map, A2, B2)
        result2 = astar2.getAStarResult()
        self.assertTrue(map.getTile(4,4) in result2)
        self.assertTrue(len(result2) ==14)
        invalid_tiles = [tile for tile in result2 if tile.terrain == 'water']
        self.assertTrue(len(invalid_tiles) == 0)



    def test_a_star_correctness(self):
        map = world_map.TileMap(7,7)
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
        astar2 = world_map._AStarNodeMap(map, A2, B2)
        result2 = astar2.getAStarResult()
        self.assertTrue(map.getTile(4,4) not in result2)
        self.assertTrue(map.getTile(5,2) in result2, [tile.x.__str__() + ", " + tile.y.__str__() for tile in result2])
        self.assertTrue(map.getTile(3,2) in result2)
        self.assertTrue(len(result2) ==10)
        invalid_tiles = [tile for tile in result2 if tile.terrain == 'water']
        self.assertTrue(len(invalid_tiles) == 0)

    def test_simple_a_star(self):
        #Now, a test of the AStarNodeMap in the most basic case.

        map = world_map.TileMap(10,10)
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


        astar = world_map._AStarNodeMap(map, A, B)
        result = astar.getAStarResult()
        self.assertTrue(result[0] == B)
        self.assertTrue(result[1].terrain == 'grass')
        self.assertTrue(result[2] == A)

    def test_contiguous_city_tiles(self):
        #FIRST:  Contiguous city tile test.
        #Question asked: Does our algorithm properly determine what cities are connectable in the most basic case?

        map = world_map.TileMap(4,4)
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

        lis = world_map.findJoinableCitySets(map)
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

    def test_road_building(self):
        map = world_map.TileMap(10,10)
        map.clearMap('water')
        map.getTile(0,0).city = 'B'
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
        map.getTile(5,0).city = 'A'
        map.drawRoadsBetweenCities()
        self.assertTrue(map.getTile(4,4).road is not None)
        self.assertTrue(map.getTile(5,0).road is not None)
        self.assertTrue(map.getTile(0,0).road is not None)


class test_perlin_noise(test.TestCase):
    def test_perlin_noise(self):
        gen = perlin_noise.perlinNoiseGenerator()
        a = gen.noise2d(2,3)
        b = gen.noise2d(2,3)

        c = gen.noise2d(3,2)
        self.assertTrue(a==b)
        self.assertTrue(a!=c)

        gen2 = mockPerlinNoise()
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

    def test_wrapping_functionality(self):
        gen = mockPerlinNoise()
        gen.wrap_x = 10
        gen.wrap_y = 10
        a = gen.noise2d(2,3)
        b = gen.noise2d(12,3)
        c = gen.noise2d(2,13)
        d = gen.noise2d(12,13)
        self.assertEqual(a,b)
        self.assertEqual(c,d)
        self.assertEqual(a,c)

        e = gen.noise2d(9,1)
        f = gen.noise2d(10,1)

        self.assertTrue(isBetween(e, f, gen.interpolate(9.5,1)))
        self.assertTrue(isBetween(gen.noise2d(9,1), gen.noise2d(0,1), gen.interpolate(9.5,1)))
        self.assertTrue

class test_spanning_tree_generation(test.TestCase):
    def test_basic_tree(self):
        t1 = world_map.Tile('grass', 1,3)
        t2 = world_map.Tile('grass', 2,10)
        t3 = world_map.Tile('grass', 2,5)

        tiles = [t1,t2,t3]
        spanning_tree = graph_tools.getMinimumSpanningTree(tiles)
        self.assertTrue(hasPairTuple(t1, t3, spanning_tree), str(spanning_tree))
        self.assertTrue(hasPairTuple(t2, t3, spanning_tree), str(spanning_tree))
        self.assertTrue(not hasPairTuple(t1, t2, spanning_tree), str(spanning_tree))

    def test_large_tree(self):
        t1 = world_map.Tile('grass', 1,3)
        t2 = world_map.Tile('grass', 2,10)
        t3 = world_map.Tile('grass', 2,5)
        t4 = world_map.Tile('grass', 3,15)
        t5 = world_map.Tile('grass', 2.1,20)
        t6 = world_map.Tile('grass', 2.5,35)

        tiles = [t1,t2,t3,t4,t5,t6]
        spanning_tree = graph_tools.getMinimumSpanningTree(tiles)

        self.assertTrue(hasPairTuple(t1, t3, spanning_tree), str(spanning_tree))
        self.assertTrue(hasPairTuple(t2, t3, spanning_tree), str(spanning_tree))
        self.assertTrue(hasPairTuple(t2, t4, spanning_tree), str(spanning_tree))
        self.assertTrue(hasPairTuple(t4, t5, spanning_tree), str(spanning_tree))
        self.assertTrue(hasPairTuple(t5, t6, spanning_tree), str(spanning_tree))

        self.assertTrue(len(spanning_tree)==5)

def hasPairTuple(a, b, container):
    return ((a,b) in container or (b,a) in container)

def isBetween(a,b, tested_value):
    if (a > b):
        a,b = b,a
    if a < tested_value < b:
        return True
    else:
        return False

class mockPerlinNoise(perlin_noise.perlinNoiseGenerator):
    def noise2d(self, x : int, y : int):
        if (self.wrap_x is not None):
            x = utils.modu(x, self.wrap_x)
        if (self.wrap_y is not None):
            y = utils.modu(y, self.wrap_y)
        return x*100 + y

def isPrettyClose(a,b):
    return (a-b)/(max(a,b)) < 0.05