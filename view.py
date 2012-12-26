__author__ = 'Aaron Kaufman'

from pygame import *
from mapgen import *
from basicmap import City
import pygame._view
import pygame.font


FPS = 15
WINDOWWIDTH = 800
WINDOWHEIGHT = 620
MAPHEIGHT = 620
MAPWIDTH = 620
BUTTONWIDTH = 90
BUTTONHEIGHT = 30
BUTTONCOLOR = (0,0,0)
WHITE = (255,255,255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   77)
GREEN     = (  0, 255,   0)
SNOW =      (233,233,255)


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
        self.x_start, self.y_start, self.x_size, self.y_size = box
        self.level = CURRENT_LEVEL
        self.function = function
        self.text = text

    def click(self, chart:MapGenerator):
        self.function(chart)

    def containsPoint(self, point:tuple):
        x,y = point
        if (x < self.x_start + self.x_size and x > self.x_start):
            if (y < self.y_start + self.y_size and y > self.y_start):
                return True
        return False

    def drawSelf(self):
        pygame.draw.rect(DISPLAYSURF, RED, pygame.Rect(self.x_start, self.y_start, self.x_size, self.y_size))

        rendered_text = BASICFONT.render(self.text, True, WHITE)
        current_rect = rendered_text.get_rect()
        current_rect.topleft = (self.x_start, self.y_start + self.y_size/2)
        DISPLAYSURF.blit(rendered_text, current_rect)



def paintControls(rendered_control_text: list, right_bounds : int, spacer : int):
    start_y = 200
    start_x = right_bounds
    width = 100
    height = 50
    box = start_x, start_y, width, height
    list = [Button(command, command.__name__, box) for command in KEYSTOFUNCTION.values()]

    i=0
    for button in list:
        assert(isinstance(button, Button))
        button.y_start += (button.y_size + 10)*i
        i+=1
        button.drawSelf()
        BUTTON_LIST.append(button)



def paintMap(map_gen : MapGenerator):
    tiles= [x[y] for y in range(0,map_gen.y_size) for x in map_gen.tile_map.xList]
    tile_size = math.floor(min(WINDOWHEIGHT/map_gen.y_size, WINDOWWIDTH/map_gen.x_size))
    for tile in tiles:
        paintTile(tile, tile_size)

    right_bounds = tile_size * map_gen.x_size
    spacer = 50
    controls_to_display = [BASICFONT.render((KEYSTOFUNCTION[control].__name__), True, WHITE)
                           for (control) in KEYSTOFUNCTION.keys()]

    paintControls(controls_to_display, right_bounds, spacer)

    pygame.display.update()
    while (True):
        pollForInput(map_gen)


def terminate():
    pygame.quit()
    sys.exit()

def paintTile(tile : Tile, tile_size : int):
    x = tile.x * tile_size
    y = tile.y * tile_size
    tileRect = pygame.Rect(x, y, tile_size, tile_size)
    pygame.draw.rect(DISPLAYSURF, Terrain().getColor(tile.terrain), tileRect)
    #Now, draw inner tile in a slightly lighter colour.
    lighterColor = brighten(Terrain().getColor(tile.terrain))
    lighterRect = pygame.Rect(x + 2, y + 2 , tile_size - 4, tile_size - 4)
    pygame.draw.rect(DISPLAYSURF, lighterColor, lighterRect)
    #Now, draw the city on the tile!  If there is one.
    if (tile.city is not None):
        assert(isinstance(tile.city, City))
        city_image = pygame.image.load(tile.city.get_pic())
        city_image = pygame.transform.scale(city_image, (tile_size, tile_size))
        DISPLAYSURF.blit(city_image, (x, y))




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

def drawContinentsByHeight(chart : MapGenerator):
    chart.clear()
    chart.drawContinentsByHeight()
    chart.main()


def craterTheLand(chart : MapGenerator):
    chart.craterTheLand()

    #Smooths the generated land by filled all water with 3-4 land neighbors as land, and all land with 3-4 water neighbors as water.
def smoothingAlgorithm(chart : MapGenerator):
    chart.smooth()





def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 9)
    pygame.display.set_caption('Map Generator!')

    global KEYSTOFUNCTION
    KEYSTOFUNCTION = {K_h : drawContinentsByHeight,
                      K_r : craterTheLand,
                      K_s : smoothingAlgorithm
    }




    chart = MapGenerator(100, 100)



    paintMap(chart)
    print('Bam!')




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
