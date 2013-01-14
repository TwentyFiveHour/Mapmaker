import struct

__author__ = 'Aaron Kaufman'
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   77)
GREEN     = (  0, 255,   0)
SNOW =      (233,233,255)


DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)

MOUNTAIN = (224, 116, 27)
PLAINS = (224, 200, 27)
SWAMP = (60, 200, 60)
WATER = (37, 27, 224)
LAVA = (245, 0, 0)
DARKWATER = (0, 10, 150)
TUNDRA =(255,255,255)
RAINFOREST = (0,200,0)
GRASSLAND = (30,244,30)
DESERT = (220, 220, 0)
FOREST = (20,100,20)

BGCOLOR = BLACK
BROWN = (139,69,19)



def rgbToHex(rgb):
    return '#%02x%02x%02x' % rgb

rgbToHex(BROWN)