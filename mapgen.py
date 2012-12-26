'''
Created on Aug 11, 2012

@author: Aaron Kaufman
'''
import operator
from enums import Terrain
from random import randrange, randint
import math
import random, sys
import random, pygame, sys
from basicmap import TileMap
from pygame.locals import *
from basicmap import Tile
from collections import Counter
import basicmap
from basicmap import WHITTAKER_MAP
import utils
WATER = "water"
LAND = "land"
MOUNTAIN = "mountain"
PLAINS = "plains"
GRASS = "grass"
DARK_WATER = 'dark water'
SNOW = "snow"

WATER_DICT = {WATER : WATER,  'dark water' : WATER}
WATER_DICT.setdefault(LAND)
    
    

#             R    G    B


class MapGenerator(object):
    '''
    classdocs
    '''
    def __init__(self, x_size=100, y_size=100):
        self.continent_size = 14
        self.tile_map=TileMap(x_size, y_size)
        self.continents_dict = {}
        self.x_size = x_size
        self.y_size = y_size
        self.smooth()



    TERRAIN_LIST = WHITTAKER_MAP.values()

    def getRandomCoords(self):
        x = randrange(0, self.x_size)
        y = randrange(0, self.y_size)
        return (x,y)
    
    def getRandomDir(self):
        x= random.randint(-1,1)
        y = random.randint(-1,1)
        return (x,y)

    #Sets all tiles to one terrain type
    def clearAllTerrain(self, terrain:str):
        for tile in (self.getTile(x,y) for x in range(0, self.x_size) for y in range (0,self.y_size)):
            tile.terrain = terrain
            tile.city = None

        
    
    def craterTheLand(self, num_craters = -1):
        if (num_craters == -1):
            num_craters = 5
        for i in range(num_craters):
            x = randrange(0,self.x_size)
            y = randrange(0,self.y_size)
            self.crater(x,y)
            self.smooth()
            
    def crater(self, start_x, start_y, radius = -1):
        if (radius == -1):
            radius = randrange(4, 7)
        for x in range(-radius, radius + 1):
            y_max = math.floor(math.pow(math.pow(radius, 2) - math.pow(x, 2), .5))
            for y in range(-1 * y_max, y_max + 1):
                if y_max == 0:
                    break
                if (abs(y) == abs(y_max)):
                    self.getTile(start_x + x, start_y + y).terrain = MOUNTAIN
                    

    def makeCities(self):
        basicmap.makeCities(self.tile_map, 10)



        
    def clear(self):
        self.clearAllTerrain(WATER)
            

    #This method randomly slices the map in half, and raises one side.
    # The end of the algorithm simply fills the map with water until the appropriate percentage
    #of the map is ocean.
    def drawContinentsByHeight(self):
        self.tile_map.makePropertiedHeightMap("height")
        self.tile_map.performWhitakerAlgorithm()
        self.tile_map.fillWithWater(30)



    def smooth(self):
        tiles= [self.getTile(x,y) for x in range(0,self.x_size) for y in range(0,self.y_size)]
        for tile in tiles:
            x = tile.x
            y = tile.y
            neighbors=[]
            neighbors.append(self.getTile(x,y+1).terrain)
            neighbors.append(self.getTile(x, y-1).terrain)
            neighbors.append(self.getTile(x+1, y).terrain)
            neighbors.append(self.getTile(x-1,y).terrain)
            ter=tile.terrain
            histogram = Counter(neighbors)
            if histogram[tile.terrain] == 0:
                tile.terrain, temp = histogram.most_common(1).pop()



            neighbor_is_land = [WATER_DICT.get(terrain, LAND) for terrain in neighbors]
            num_waters = 0 
            for string in neighbor_is_land:
                if string == WATER:
                    num_waters+=1
            if (num_waters >=3):
                tile.terrain = WATER
                    
            
            
                   

    def createTerrainFromHeight(self, percent_ter, terrain, ideal_height):
        grass_tiles = 0
        for i in self.tile_map.xList:
            for t in i:
                t.ideal_height = ideal_height
        
        sorted_tiles = sorted([item for sublist in self.tile_map.xList for item in sublist],
                              key = self.getIdealHeightDiff)
        for t in sorted_tiles:
            if ((grass_tiles * 100.0) / (self.x_size * self.y_size) > percent_ter):
                return
            t.terrain = terrain
            grass_tiles +=1

    def getIdealHeightDiff(self, tile):
        return abs(tile.ideal_height - tile.height)
    
    def getHeight(self, tile):
        return tile.height        
    
    def createSeeds(self, num_continents):
        '''
        '''
        for i in range (num_continents):
            x = randrange(self.x_size)
            y = randrange(self.y_size)
            seed_tile = self.tile_map.getTile(x,y)
            self.continents_dict[i] = set([Tile])
            self.continents_dict[i].add(seed_tile)
            
            
  
    



    def getTile(self, x, y)-> Tile:
        return self.tile_map.getTile(utils.modu(x, self.x_size), utils.modu(y, self.y_size))



    
    def __str__(self):
        return str(self.tile_map)


def getPointsInRadius(point : tuple, radius : int):
    """
    :rtype : int
    """
    start_x, start_y = point
    points = []
    for x in range(-radius, radius + 1):
        y_max = math.floor(math.pow(math.pow(radius, 2) - math.pow(x, 2), .5))
        for y in range(-y_max, y_max + 1):
            point = (start_x + x, start_y + y)
            points.append(point)
           
    return points;
