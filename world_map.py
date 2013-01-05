'''
Created on Aug 31, 2012

@author: Aaron Kaufman
'''
import city
import collections
import heapq
import math
import colors as co
import terrain as ter
import utils
from random import choice
import perlin_noise
import cProfile
import graph_tools
import basic_map


TEMP_MAP = {15:"cold",
                   55:"medium",
                   100:"warm"}

RAIN_MAP = {33:"wet",
                66: "medium",
                100: "dry"}

WHITTAKER_MAP = {("wet", "cold"): "tundra",
                 ("medium","cold"): "tundra",
                 ("dry","cold"):  "tundra",
                 ("wet", "medium"): "swamp",
                 ("medium","medium"): "forest",
                 ("dry","medium"): "grass",
                 ("wet", "warm"): "rainforest",
                 ("medium", "warm"):  "plains",
                 ("dry", "warm"):  "desert"}

#Terrain generation parameters

PERCENT_WATER = 40
POLAR_BIAS = 60
ISLAND_BIAS = -40
ISLANDS_X = 1
ISLANDS_Y = 1
#Total islands = islands_x * islands_y
LAND="land"

WATER_DICT = {"water" : ter.WATER}
WATER_DICT.setdefault(LAND)



class WorldMap( basic_map.TileMap):

    def __init__(self, max_x = 50, max_y =50):
        basic_map.TileMap.__init__(self, max_x, max_y)
        self.islands_x = ISLANDS_X
        self.islands_y = ISLANDS_Y
        self.polar_bias = POLAR_BIAS
        self.percent_water = PERCENT_WATER
        #used when we don't have wrapping enabled.
        self.IMPASSIBLE_TILE = basic_map.Tile(ter.IMPASSIBLE, -1, -1)
        self.smoothness = 10




    def remake(self):
        '''
        Builds out the map.
        '''
        self.clearMap("water")
        self.makePropertiedHeightMap("height", smoothness = self.smoothness, bias = islandBiasFunction, bias_amplitude = ISLAND_BIAS)
        self.performWhitakerAlgorithm()
        self.fillWithWater(30)
        self.makeCities(10)
        self.drawRoadsBetweenCities()


    def drawRoadsBetweenCities(self):
        contiguous_city_tiles_list = findJoinableCitySets(self)
        for list in contiguous_city_tiles_list:
            roads_to_draw = graph_tools.getMinimumSpanningTree(list)
            for city_pair in roads_to_draw:
                tile_list = getClosestRoute(self, city_pair[0], city_pair[1])
                for tile in tile_list:
                    tile.road = "road"


    def performWhitakerAlgorithm(self):
        """
        Creates maps of temperature and rainfall, and uses those to dictate terrain types.
        """
        self.makePropertiedHeightMap("temperature", smoothness = self.smoothness, bias = polarBiasFunction, bias_amplitude = POLAR_BIAS)
        self.declareEffectiveProperties("temperature",TEMP_MAP,"temp_string")
        self.makePropertiedHeightMap("rainfall", smoothness = self.smoothness)
        self.declareEffectiveProperties("rainfall",RAIN_MAP,"rain_string")
        for tile in (self.getTile(x, y) for x in range(0,self.max_x) for y in range(0, self.max_y)):
            tup = (tile.rain_string, tile.temp_string)
            tile.terrain = WHITTAKER_MAP[tup]


    def getTile(self, x, y) -> basic_map.Tile:
        if (self.wrap_x):
            x = utils.modu(x, self.max_x)
        if (self.wrap_y):
            y = utils.modu(y, self.max_y)

        if not (0<=x<self.max_x):
            return self.IMPASSIBLE_TILE
        if not (0<=y<self.max_y):
            return self.IMPASSIBLE_TILE
        return self.xList[x][y]

    def __str__(self):
        temp = ''
        for x in range(self.max_x):
            for y in range(self.max_y):
                temp = temp + str(self.getTile(x, y))
            temp = temp + '\n'
        return temp




    def makePropertiedHeightMap(self, the_property, smoothness, bias = None, bias_amplitude = None):
        """
        #This is a method to create a height map on the tilemap with any property,
        # using perlin noise.
        #(Ex: the_property can be "height", "temperature", or anything else.)
        #This new property is placed into the attributes of each tile with the new value.
        #"Smoothness" defines how many tiles exist between two perlin noise spikes.
        "Bias" refers to a function that can modify the resulting height according to the tile's spatial location.
        "Bias_amplitude" refers to how much of an impact this will have on the resulting heightmap.

        """

        gen = self.buildPerlinNoiseGenerator(smoothness)

        tiles_list = [self.getTile(x,y) for x in range(0,self.max_x) for y in range(0, self.max_y)]
        for tile in tiles_list:
            x = tile.x
            y = tile.y

            p_x = x/smoothness
            p_y = y/smoothness

#            if (self.wrap_x):
 #               p_x = utils.modu(p_x, grid_size_x)
  #          if (self.wrap_y):
   #             p_y = utils.modu(p_y, grid_size_y)
            bias_value = 0
            if bias is not None:
                assert(bias_amplitude is not None)
                bias_value = bias(self, tile, bias_amplitude)
            else:
                assert(bias_amplitude is None)
            value = gen.interpolate(p_x,p_y) + bias_value
            tile.__setattr__(the_property, value)



    def buildPerlinNoiseGenerator(self, smoothness) -> perlin_noise.perlinNoiseGenerator:
        """
        Creates a perlin noise generator fitting the requirements of this world map.
        """
        grid_size_x = self.max_x/smoothness
        grid_size_y = self.max_y/smoothness
        if (grid_size_x < 1):
            grid_size_x = 1
        if (grid_size_y < 1):
            grid_size_y = 1

        gen = perlin_noise.perlinNoiseGenerator()
        gen.wrap_x = grid_size_x
        gen.wrap_y = grid_size_y
        return gen

    def declareEffectiveProperties(self, property_name, percentile_to_title, title_name):
        """
        #Maps out the property given to a percentile.
        #percentile_to_title is a dictionary
        #Ex:  99 percentile covers the top 99% of the map.
        #title refers to the name of the property given to the tile.
        #property refers to the field that the title is derived from.
        For example, the property could be temperature, and that could correspond to the titles ("title_name")
        "warm", "cold", or "medium" depending on percentile.
        """
        flattened_tile_list = [self.getTile(x,y) for x in range(0, self.max_x) for y in range(0, self.max_y)]
        for tile in flattened_tile_list:

            tile.sort_key = tile.__getattribute__(property_name)

        key_list = percentile_to_title.keys()
        key_list = sorted(key_list)

        flattened_tile_list.sort(key = basic_map.Tile.getSortKey, reverse = False)
        current = 0
        for tile in flattened_tile_list:
            if len(key_list)==0:
                return
            current+=1
            current_percent_finished = current/len(flattened_tile_list)*100
            if (key_list[0] < current_percent_finished):
                key_list.pop(0)    #If we've finished with the current key, chuck it from the stack!
            tile.__setattr__(title_name, percentile_to_title.get(key_list[0]))



    def fillWithWater(self, percent_ter):
        flattened_tile_list = [self.getTile(x,y) for x in range(0, self.max_x) for y in range(0, self.max_y)]
        for tile in flattened_tile_list:
            tile.sort_key = tile.height


        flattened_tile_list.sort(key = basic_map.Tile.getSortKey, reverse = False)
        count=0
        for tile in flattened_tile_list:
            count+=1
            tile.terrain = 'water'
            if (count/len(flattened_tile_list)*100 > percent_ter):
                return

    def makeMountainRanges(self):
        """
        Takes the highest peaks that already exist and builds mountain ranges out of them.
        They attempt to go the direction leading to the highest-altitude mountain ranges, but stay going in
        one direction (to avoid 'blobs' of mountains).
        """
        mountain_list = [self.getTile(x,y) for x in range(0, self.max_x) for y in range(0, self.max_y) if self.getTile(x,y).terrain == ter.MOUNTAIN]



    def clearMap(self, terrain):
        """
        Resets all land to a given terrain and sets the cities and roads to null.  (For use during testing.)
        """
        tile_list = [self.getTile(x,y) for x in range(0, self.max_x) for y in range(0, self.max_y)]
        for tile in tile_list:
            tile.terrain = terrain
            tile.city = None
            tile.road = None

    def makeCities(self, num_cities : int):
        land_tiles = [self.getTile(x,y) for x in range(0,self.max_x) for y in range(0, self.max_y)
                      if WATER_DICT.get(self.getTile(x,y).terrain, LAND) == LAND]
        city_tiles = [choice(land_tiles) for x in range (0,num_cities)]
        for tile in city_tiles:
            tile.city = city.City()





#START BIAS FUNCTIONS
#These must demand uniform parameters
#And be reasonably efficient, as they are called for every tile.


def islandBiasFunction(tile_map:WorldMap, tile:basic_map.Tile, amplitude = ISLAND_BIAS):
    """
    returns a higher value at the center of the map, and a  lower value at the edges.
    Creates a number of elevated points equal to the value of (num_hills_x * num_hills_y)
    This corresponds to a number of islands, if we're using this to increment our Height values.
    Note: Islands are not guaranteed separation.  Amount of separation depends on % of water in the map.
    Given a negative amplitude, it will generate a central lake.
    """
    num_hills_x = 1
    num_hills_y = 1
    x = tile.x
    y = tile.y
    max_x = tile_map.max_x
    max_y = tile_map.max_y


    cos_result_x = -math.cos(x/max_x * num_hills_x * 2 * math.pi)*amplitude
    cos_result_y = -math.cos(y/max_y * num_hills_y * 2 * math.pi)*amplitude
    return (cos_result_x + cos_result_y)/2

def polarBiasFunction(tile_map:WorldMap, tile:basic_map.Tile, amplitude = POLAR_BIAS):
    """
    #Causes cold temperatures at poles, and warm temps at the equator (assuming amplitude is positive).
    """
    equator = tile_map.max_y/2
    return (equator - math.fabs(equator-tile.y)) / equator * amplitude




PASSABLE_DICT = {ter.MOUNTAIN : False,
                 ter.WATER : False,
                 ter.IMPASSIBLE: False}

def _getPassable(t:basic_map.Tile):
    return PASSABLE_DICT.setdefault(t.terrain, True)


def findJoinableCitySets(map: WorldMap):
    """
    #returns a set of cities connected to each other by passable terrain
    """

    city_tile_set = [map.getTile(x,y) for x in range(0, map.max_x) for y in range(0,map.max_y)
                     if map.getTile(x,y).city is not None]
    full_tile_set = [map.getTile(x,y) for x in range(0,map.max_x) for y in range(0,map.max_y)]
    for tile in full_tile_set:
        tile._has_been_visited = False
    previously_encountered_city_tiles = []
    contiguous_city_list_list = []
    for city_tile in city_tile_set:
        if city_tile in previously_encountered_city_tiles:
            continue
            #tracks contiguous tiles found for this city_tile_set.
        #open_set acts as a queue.
        cont_cities = [] #This is what we'll be "returning" from the loop: each list of contiguous city tiles goes
        #into the cont_cities list.
        open_set = collections.deque()
        open_set.appendleft(city_tile)
        while (open_set):
            t = open_set.pop()
            x=t.x
            y=t.y
            if not _getPassable(t):  #don't use this tile if we can't pass it.
                continue
            if (True is t._has_been_visited): # don't use this tile if it has been visited.
                continue
            else:
                if (t in open_set):
                    continue
                t._has_been_visited = True
                n = map.getTile(x,y+1)
                s = map.getTile(x,y-1)
                e = map.getTile(x+1,y)
                w = map.getTile(x-1,y)
                _addTileIfAdmissible(open_set, n)
                _addTileIfAdmissible(open_set, s)
                _addTileIfAdmissible(open_set, e)
                _addTileIfAdmissible(open_set, w)
                if (t.city is not None):
                    cont_cities.append(t)
                    previously_encountered_city_tiles.append(t)
        contiguous_city_list_list.append(cont_cities)
    return contiguous_city_list_list


def _addTileIfAdmissible(deq:collections.deque, t: basic_map.Tile):
    if (_getPassable(t) and not t._has_been_visited):
        if t not in deq:
            deq.appendleft(t)



class _RoadNode(object):
    """
    #heuristic refers to linear distance to goal node.
    #The first node should have a parent of None.
    #Parent is the node this node was spawned off of; used for ancestry.
    """
    def __init__(self, tile : basic_map.Tile, parent, heuristic):
        self.tile = tile
        self.parent = parent
        self.heuristic = heuristic
        if parent is not None:
            if tile.road == "road":
                self.distance = parent.distance
            elif tile.road is None:
                self.distance = parent.distance + 1
            else:
                assert False
        else:
            self.distance = 0


    def getAncestry(self) -> list:
        nodes = []
        current = self
        while current is not None:
            nodes.append(current.tile)
            current = current.parent
        return nodes

    def __lt__(node1,node2):

        return (node1.heuristic + node1.distance) < (node2.heuristic + node2.distance)



class _AStarNodeMap(object):
    """
    #Represents the A-Star algorithm on a tiled map
    """
    def __init__(self, map : WorldMap, start:basic_map.Tile, goal:basic_map.Tile):

        self.start = start
        self.already_hit = []
        self.open_set = []
        heapq.heapify(self.open_set)
        heapq.heappush(self.open_set, _RoadNode(start, None, 1))
        self.goal = goal
        self.map = map


    def getLinearDistanceToGoal(self, x, y) -> int:
        """

        #Acts as heuristic for A-star algorithm.  Gets distance between given point and the goal.
        """
        map = self.map
        return utils.getLinearDistance(basic_map.Tile("placeholder",x,y), self.goal, map.max_x, map.max_y, map.wrap_x, map.wrap_y)


    def buildAdjacentNodes(self, parent:_RoadNode):
        """
        Builds nodes adjacent to the current tile if the current tile is "valid", and adds them to the open set.
        """
        x = parent.tile.x
        y = parent.tile.y
        n = self.map.getTile(x,y+1)
        s = self.map.getTile(x,y-1)
        e = self.map.getTile(x+1,y)
        w = self.map.getTile(x-1,y)

        new_tiles = [n,s,e,w]
        for tile in new_tiles:
            if ((tile.x,tile.y) not in self.already_hit and _getPassable(tile)):
                heapq.heappush(self.open_set, _RoadNode(tile, parent, self.getLinearDistanceToGoal(tile.x, tile.y)))
                tup = (tile.x, tile.y)
                self.already_hit.append(tup)


    def getAStarResult(self) -> list:
        current = _RoadNode(self.start, None, 0)
        while current.tile is not self.goal:
            current = heapq.heappop(self.open_set)
            self.buildAdjacentNodes(current)
        return current.getAncestry()

def getClosestRoute(map : WorldMap, start: basic_map.Tile, goal: basic_map.Tile):
    """
    Creates an A* node map and retrieves the result.
    This is for the roadbuilding algorithm--
    It treats all passable tiles the same,
    except that it minimizes the total amount of road constructed
    by re-using existing roads.
    """
    node_map = _AStarNodeMap(map,start,goal)
    return node_map.getAStarResult()

#benchmark: 17 secs with bias function
#14 without

if __name__ == '__main__':
    cProfile.run('TileMap(200,200)', )
