'''
Created on Aug 31, 2012

@author: Aaron Kaufman
'''

from random import randint
from random import randrange
import math

import utils
from random import choice
import perlin_noise
import cProfile
        
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

ISLANDS_X = 1
ISLANDS_Y = 1
#Total islands = islands_x * islands_y



WATER = "water"
LAND = "land"
MOUNTAIN = "mountains"
PLAINS = "plains"
GRASS = "grass"
DARK_WATER = 'dark water'

WATER_DICT = {WATER : WATER,  'dark water' : WATER}
WATER_DICT.setdefault(LAND)

class Tile(object):
    '''
    classdocs
    This represents a tile.
    Tiles have an associated Continent and an associated TerrainType.
    '''


    def __init__(self, terrain, x, y, city = None):
        '''
        Constructor
        '''
        self.terrain = terrain
        self.x = x
        self.y = y
        self.height = 0
        self.sort_key = 0
        self.city = city
        assert(self.city is City or self.city is None)
    def __str__(self):
        if self.city is  not None:
            return self.city
        else:
            return self.terrain



    def getProperty(self, property_name):
        return self.__getattribute__(property_name)

    def getSortKey(self):
        return self.sort_key





class City(object):

    def get_pic(self):
        return 'images/b_rook.png'


class TileMap(object):

    def __init__(self, max_x = 50, max_y =50):
        '''
        Constructor
        '''
        self.max_y = max_y
        self.max_x = max_x
        self.xList = []
        for x in range(0, max_x):
            yList = []
            self.xList.append(yList)
            for y in range(0, max_y):
                yList.append(Tile(WATER, x, y))

        self.makePropertiedHeightMap("height", bias = islandBiasFunction, bias_amplitude = 40)
        self.performWhitakerAlgorithm()
        self.fillWithWater(30)
        makeCities(self, 10)
        
    def performWhitakerAlgorithm(self):
        self.makePropertiedHeightMap("temperature", smoothness = 20, bias = polarBiasFunction, bias_amplitude = 80)
        self.declareEffectiveProperties("temperature",TEMP_MAP,"temp_string")
        self.makePropertiedHeightMap("rainfall", smoothness = 20)
        self.declareEffectiveProperties("rainfall",RAIN_MAP,"rain_string")
        for tile in (self.getTile(x, y) for x in range(0,self.max_x) for y in range(0, self.max_y)):
            tup = (tile.rain_string, tile.temp_string)
            tile.terrain = WHITTAKER_MAP[tup]

    #essentially performs the function {object.property+=value}.
    #with no value parameter, it is functionally {object.property++}
    #Return type:  Void.
    @staticmethod
    def incrementGenericProperty(object, the_property, value = 1):
        current_val = object.__getattribute__(the_property)
        current_val += value
        object.__setattr__(the_property, current_val)
        

    def getTile(self, x, y) -> Tile:
        x = utils.modu(x, self.max_x)
        y = utils.modu(y, self.max_y)
        return self.xList[x][y]
    
    def __str__(self):
        temp = ''
        for x in range(self.max_x):
            for y in range(self.max_y):
                temp = temp + str(self.getTile(x, y))
            temp = temp + '\n'
        return temp
        
        
    #This is a method to create a height map on the tilemap with any property,
    # using perlin noise.
    #(Ex: the_property can be "height", "temperature", or anything else.)
    #This new property is instilled into each tile with a new value.
    #"Smoothness" defines how many tiles exist between two perlin noise spikes.
    #gen_cache


    def makePropertiedHeightMap(self, the_property, smoothness = 10, wrap_x = False, wrap_y = False, bias = None, bias_amplitude = None):

        grid_size_x = math.floor(self.max_x/smoothness)
        grid_size_y = math.floor(self.max_y/smoothness)
        gen = perlin_noise.perlinNoiseGenerator()

        tiles_list = [self.getTile(x,y) for x in range(0,self.max_x) for y in range(0, self.max_y)]
        for tile in tiles_list:
            x = tile.x
            y = tile.y


            p_x = x/smoothness
            p_y = y/smoothness

            #if (wrap_x):
            #    p_x = utils.modu(p_x, grid_size_x)
            #if (wrap_y):
            #    p_y = utils.modu(p_y, grid_size_y)
            bias_value = 0
            if bias is not None:
                assert(bias_amplitude is not None)
                bias_value = bias(self, tile, bias_amplitude)


            tile.__setattr__(the_property, gen.interpolate(p_x,p_y) + bias_value)




        #Maps out the property given to a given percentile.
        #percentile_to_title is a dictionary
    #Ex:  99 percentile covers the top 99% of the map.
    #title refers to the name of the property given to the tile.
    #property refers to the field that the title is derived from.
    def declareEffectiveProperties(self, property_name, percentile_to_title, title_name):
        flattened_tile_list = [self.getTile(x,y) for x in range(0, self.max_x) for y in range(0, self.max_y)]
        for tile in flattened_tile_list:
            
            tile.sort_key = tile.__getattribute__(property_name)
        
        key_list = percentile_to_title.keys()
        key_list = sorted(key_list)
        
        flattened_tile_list.sort(key = Tile.getSortKey, reverse = False)
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
        
        
        flattened_tile_list.sort(key = Tile.getSortKey, reverse = False)
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
        mountain_list = [self.getTile(x,y) for x in range(0, self.max_x) for y in range(0, self.max_y) if self.getTile(x,y).terrain == MOUNTAIN]

        return




def makeCities(tile_map : TileMap, num_cities : int):
    land_tiles = [tile_map.getTile(x,y) for x in range(0,tile_map.max_x) for y in range(0, tile_map.max_y)
                  if WATER_DICT.get(tile_map.getTile(x,y).terrain, LAND) == LAND]
    city_tiles = [choice(land_tiles) for x in range (0,num_cities)]
    for tile in city_tiles:
        tile.city = City()





#START BIAS FUNCTIONS
#These must demand uniform parameters
#And be reasonably efficient, as they are called for every tile.

def islandBiasFunction(tile_map:TileMap, tile:Tile, amplitude):

    num_hills_x = 1
    num_hills_y = 1
    x = tile.x
    y = tile.y
    max_x = tile_map.max_x
    max_y = tile_map.max_y


    cos_result_x = -math.cos(x/max_x * num_hills_x * 2 * math.pi)*amplitude
    cos_result_y = -math.cos(y/max_y * num_hills_y * 2 * math.pi)*amplitude
    return (cos_result_x + cos_result_y)/2

#Causes cold temperatures at poles, and warm temps at the equator.
def polarBiasFunction(tile_map:TileMap, tile:Tile, amplitude):
    equator = tile_map.max_y/2
    return (equator - math.fabs(equator-tile.y)) / equator * amplitude


if __name__ == '__main__':
    cProfile.run('TileMap(200,200)', )

#benchmark: 17 secs with bias function
#14 without
