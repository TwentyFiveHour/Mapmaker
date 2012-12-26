'''
Created on Aug 12, 2012

@author: Aaron Kaufman
'''

#            R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   77)
GREEN     = (  0, 255,   0)
SNOW =      (233,233,255)


DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
   
MOUNTAIN = (224, 116, 27)
PLAINS = (224, 224, 27)
GRASSLAND = (60, 224, 27)
WATER = (37, 27, 224)
LAVA = (245, 0, 0)
DARKWATER = (0, 10, 150)
TUNDRA =(255,255,255)
RAINFOREST = (0,211,0)
FOREST = (30,244,30)
DESERT = (220, 220, 0)
SWAMP = (20,100,20)

BGCOLOR = BLACK

class Terrain(object):
    '''
    This class serves two purposes: First, it enumerates the different long and short 
    string values for terrain.  Second, it maps the short version of the terrain names
    to the long version.  (The short is used in creating a functional map with print
    statements.)
    '''

    
    

    def __init__(self):
        self.Grass = 'grass'
        self.Water = 'water'
        self.Plains = 'plains'
        self.Mountain= 'mountain'
        self.Lava = 'lava'
        self.DarkWater = 'dark water'
        self.Snow = 'snow'
        self.Desert ='desert'
        self.Tundra = 'tundra'
        self.Forest = 'forest'
        self.Swamp = 'swamp'
        self.RainForest = 'rainforest'
        
        self.SLava = 'l'
        self.SGrass = 'g'
        self.SWater = 'w'
        self.SPlains = 'p'
        self.SMountain = 'm'
        self.SDarkWater = 'd'
        #Translator turns long forms into short forms.
        #NOTE:  SHORT FORM IS CANONICAL FOR FUNCTIONS.
        
        self.translator = {}
        self.translator[self.Lava] = self.SLava
        self.translator[self.Grass] = self.SGrass
        self.translator[self.Water] = self.SWater
        self.translator[self.Plains] = self.SPlains
        self.translator[self.Mountain] = self.SMountain
        self.translator[self.DarkWater] = self.SDarkWater
        
        #shortToLong turns short forms into long.
        self.shortToLong = {}
        
        self.longToColor = {}
        self.longToColor[self.Grass] = GRASSLAND
        self.longToColor[self.Plains] = PLAINS
        self.longToColor[self.Mountain] = MOUNTAIN
        self.longToColor[self.Water] = WATER
        self.longToColor[self.Lava] = LAVA
        self.longToColor[self.DarkWater] = DARKWATER
        self.longToColor[self.Snow] = SNOW
        self.longToColor[self.Desert] = DESERT
        self.longToColor[self.Forest] = FOREST
        self.longToColor[self.RainForest] = RAINFOREST
        self.longToColor[self.Tundra]= TUNDRA
        self.longToColor[self.Swamp] = SWAMP

        
        for key in self.translator.keys():
            self.shortToLong[self.translator[key]] = key
        
    
    def getShort(self, terrain):
       
        s = self.translator[terrain]
        return s
    
    def getLong(self, terrain):
        return self.shortToLong[terrain]

    def getColor(self, terrainLong):
        return self.longToColor[terrainLong]
    
    


