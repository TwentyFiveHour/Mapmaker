__author__ = 'Aaron Kaufman'

from pygame import *
from city import City
import world_map as bmap
import pygame._view
import pygame.font
import math
import terrain
import sys
import colors as co
import world_map
import basic_map as bmap

FPS = 15
WINDOWWIDTH = 800
WINDOWHEIGHT = 620
MAPHEIGHT = 620
MAPWIDTH = 620
BUTTONWIDTH = 90
BUTTONHEIGHT = 30
BUTTONCOLOR = (0,0,0)

##BUTTON-CREATION CODE.  Involves usage of "level" to
# determine which buttons are currently active, for hierarchical menus.

display_all_levels = True
BUTTON_LIST = []
CURRENT_LEVEL = 1
#Box is a tuple containing in order (xstart, ystart, xsize, ysize)


def destroyHigherButtons():
    for button in BUTTON_LIST:
        if (button.level > CURRENT_LEVEL):
            BUTTON_LIST.remove(button)

def addButton(button):
    BUTTON_LIST.add(button)

def raiseLevel():
    CURRENT_LEVEL+=1

class Button(object):


    def __init__(self, function, text:str, box: tuple ):
        self.x_start, self.y_start, self.max_x, self.max_y = box
        self.level = CURRENT_LEVEL
        self.function = function
        self.text = text

    def click(self, chart:world_map.WorldMap):
        self.function(chart)

    def containsPoint(self, point:tuple):
        x,y = point
        if (x < self.x_start + self.max_x and x > self.x_start):
            if (y < self.y_start + self.max_y and y > self.y_start):
                return True
        return False

    def drawSelf(self):
        pygame.draw.rect(DISPLAYSURF, co.RED, pygame.Rect(self.x_start, self.y_start, self.max_x, self.max_y))

        rendered_text = BASICFONT.render(self.text, True, co.WHITE)
        current_rect = rendered_text.get_rect()
        current_rect.topleft = (self.x_start, self.y_start + self.max_y/2)
        DISPLAYSURF.blit(rendered_text, current_rect)

def createButtonList( right_bounds : int):
    start_y = 200
    start_x = right_bounds
    width = 100
    height = 50
    box = start_x, start_y, width, height
    list = [Button(command, command.__name__, box) for command in KEYSTOFUNCTION.values()]
    for button in list:
        BUTTON_LIST.append(button)

def paintControls():

    i=0
    for button in BUTTON_LIST:
        assert(isinstance(button, Button))
        button.y_start += (button.max_y + 10)*i
        i+=1
        button.drawSelf()

def paintLegend(dictionary : dict, right_bounds : int, spacer: int):
    start_y = 250 + len(BUTTON_LIST) * 50
    start_x = right_bounds
    start_rectangle_x = right_bounds + 70
    key_list = [key for key in terrain.NAME_TO_COLOR.keys()]
    for key in key_list:
        pygame.draw.rect(DISPLAYSURF, terrain.NAME_TO_COLOR[key], pygame.Rect(start_rectangle_x, start_y, 10, 10))
        rendered_text = BASICFONT.render(str(key) + " : ", True, co.WHITE)
        current_rect = rendered_text.get_rect()
        current_rect.topleft = (start_x, start_y)
        DISPLAYSURF.blit(rendered_text, current_rect)
        start_y += 20


def paintMap(tile_map : world_map.WorldMap):
    tiles= [x[y] for y in range(0,tile_map.max_y) for x in tile_map.tile_grid]
    tile_size = math.floor(min(WINDOWHEIGHT/tile_map.max_y, WINDOWWIDTH/tile_map.max_x))
    for tile in tiles:
        paintTile(tile, tile_size, tile_map)

    right_bounds = tile_size * tile_map.max_x
    spacer = 50
    controls_to_display = [BASICFONT.render((KEYSTOFUNCTION[control].__name__), True, co.WHITE)
                           for (control) in KEYSTOFUNCTION.keys()]

    paintControls()
    paintLegend(terrain.NAME_TO_COLOR, right_bounds, spacer)

    pygame.display.update()
    while (True):
        pollForInput(tile_map)


def terminate():
    pygame.quit()
    sys.exit()

def paintTile(tile : bmap.Tile, tile_size : int, map : world_map.WorldMap):
    x = tile.x * tile_size
    y = tile.y * tile_size
    tile_rect = pygame.Rect(x, y, tile_size, tile_size)
    pygame.draw.rect(DISPLAYSURF, terrain.NAME_TO_COLOR[tile.terrain], tile_rect)
    #Now, draw inner tile in a slightly lighter colour.
    lighterColor = brighten(terrain.NAME_TO_COLOR[tile.terrain])
    lighterRect = pygame.Rect(x + 2, y + 2 , tile_size - 4, tile_size - 4)
    pygame.draw.rect(DISPLAYSURF, lighterColor, lighterRect)

    drawRoads(tile_rect, map, tile)

    #Now, draw the city on the tile!  If there is one.
    if (tile.city is not None):
        assert(isinstance(tile.city, City))
        city_image = pygame.image.load(tile.city.get_pic())
        city_image = pygame.transform.scale(city_image, (tile_size, tile_size))
        DISPLAYSURF.blit(city_image, (x, y))

def drawRoads(tile_rect : pygame.Rect, map: world_map.WorldMap, tile:bmap.Tile):
    """
    draws the road if there is one.  Extends from current tile to adjacent tiles with roads
    """
    center = tile_rect.center
    midtop = tile_rect.midtop
    midbottom = tile_rect.midbottom
    midleft = tile_rect.midleft
    midright = tile_rect.midright
    x = tile.x
    y = tile.y
    line_width = 3
    if tile.road is not None:
        if (map.getTile(x+1,y).road is "road"): #to the right
            pygame.draw.line(DISPLAYSURF, co.BROWN, center, midright, line_width)
        if (map.getTile(x-1,y).road is "road"): #to the left
            pygame.draw.line(DISPLAYSURF, co.BROWN, center, midleft, line_width)
        if (map.getTile(x,y-1).road is "road"): #to  up
            pygame.draw.line(DISPLAYSURF, co.BROWN, center, midtop, line_width)
        if (map.getTile(x,y+1).road is "road"): #to  down
            pygame.draw.line(DISPLAYSURF, co.BROWN, center, midbottom, line_width)


def remake(map : world_map.WorldMap):
    map.remake()

#Accepts a RGB tuple, and returns an RGB tuple that's a bit brighter.
def brighten(color):
    r,g,b = color
    r += 10
    g += 10
    b += 10
    val = []
    for i in (r,g,b):
        if i >255:
            i = 255
        elif i < 0:
            i = 0
        val.append(i)

    return (val[0],val[1],val[2])

    #Smooths the generated land by filled all water with 3-4 land neighbors as land, and all land with 3-4 water neighbors as water.

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 9)
    pygame.display.set_caption('Map Generator!')

    global KEYSTOFUNCTION
    KEYSTOFUNCTION = {K_r : remake}

    chart = world_map.WorldMap(50, 50)

    tile_size = math.floor(min(WINDOWHEIGHT/chart.max_y, WINDOWWIDTH/chart.max_x))

    right_bounds = tile_size * chart.max_x

    createButtonList(right_bounds)
    paintMap(chart)



def pollForInput(chart):
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        elif event.type == KEYDOWN:
            try:
                KEYSTOFUNCTION[event.key](chart)
            except:
                return
            paintMap(chart)
        elif event.type == MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for button in BUTTON_LIST:
                if (button.level == CURRENT_LEVEL and button.containsPoint(pos)):
                    button.click(chart)
                    paintMap(chart)


if __name__ == '__main__':
    main()
