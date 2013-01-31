import tkinter as tk
from tkinter import ttk
import world_state
import math
import terrain as ter
import colors
import basic_map
import utils
from tkinter import messagebox

CANVAS_WIDTH = 500
CANVAS_HEIGHT = 500
NEARBY_TILES = utils.NEARBY_TILE_COORDS

root = tk.Tk()
BOARD_STATE = world_state.WorldState()



def repaintAfterOperation(f):
    def wrapper(self, *args):
        return_val = f(self, *args)
        self.painter.repaint()
        return return_val
    return wrapper



class MainFrame(object):
    def __init__(self):





        self.root = root
        content = ttk.Frame(root)
        canvas = tk.Canvas(content, borderwidth=5, relief="sunken", width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
        namelbl = ttk.Label(content, text="Name")
        name = ttk.Entry(content)
        content.grid(column = 0, row = 0)
        canvas.grid(column = 0, row = 0, columnspan = 10, rowspan = 10)
        info_frame = ttk.Frame(content,borderwidth = 5, width = 200, height = 500)
        info_frame.grid(column = 11, row = 0, columnspan = 3, rowspan = 9)

        game = world_state.WorldState()
        painter = CanvasPainter(canvas)
        self.canvas = canvas
        self.painter = painter
        self.context = ViewContext(map = BOARD_STATE, painter = painter)
        self.content = content
        label = ttk.Label(info_frame, text='Full name:')
        resultsContents = tk.StringVar()
        label['textvariable'] = resultsContents
        resultsContents.set('View Type')
        #View buttons
        view_level = tk.StringVar()
        view_level.set(world_state.ABOVE_GROUND)
        above_ground = ttk.Radiobutton(info_frame, text='Above Ground', variable=view_level, value=world_state.ABOVE_GROUND,
        command = lambda : self.select_map(view_level))
        below_ground = ttk.Radiobutton(info_frame, text='Under Ground', variable=view_level, value=world_state.BELOW_GROUND,
        command = lambda : self.select_map(view_level))


        zoom = tk.IntVar()
        zoom.set(15)

        zoom_settings = {1: 8,2:10,3:15,4:30}
        for setting_num in zoom_settings:
            button = ttk.Radiobutton(info_frame, text=setting_num, variable=zoom, value=zoom_settings[setting_num],
                command = lambda : self.setTileSize(zoom.get()))
            button.grid(column = 11, row = 4 + setting_num)

        #Paint bindings

        self.canvas.bind("<Button-1>", self.context.clickOnCanvas)

        #paint dropdown
        values = tuple(ter.NAME_TO_COLOR.keys())
        terrain_selected = tk.StringVar()
        terrain_selected.set(ter.GRASS) # initial value

        option = tk.OptionMenu(info_frame, terrain_selected, *values)
        option.grid(column = 11, row = 10)
        terrain_selected.trace("w",self.context.changeTerrain)

        #keybindings for motion
        root.bind("<Up>", self.up)
        root.bind("<Down>", self.down)
        root.bind("<Left>", self.left)
        root.bind("<Right>", self.right)

        remake_button =ttk.Button(info_frame, text = 'Remake', command = self.restart)

        label.grid(column = 11,row=0)
        above_ground.grid(column = 11, row = 1)
        below_ground.grid(column = 11, row = 2)
        remake_button.grid(column = 11, row = 3 )

        painter.repaint()

        root.mainloop()

    @repaintAfterOperation
    def restart(self):
        BOARD_STATE.restart()

    @repaintAfterOperation
    def select_map(self, var):
        self.painter.mode = var.get()

    @repaintAfterOperation
    def down(self, event):
        x,y = self.painter.current_focus
        self.painter.current_focus = (x, y + math.floor(self.painter.getWindowHeightInTiles()/5))

    @repaintAfterOperation
    def up(self, event):
        x,y = self.painter.current_focus
        self.painter.current_focus = (x, y - math.floor(self.painter.getWindowHeightInTiles()/5))

    @repaintAfterOperation
    def left(self, event):
        x,y = self.painter.current_focus
        self.painter.current_focus = (x - math.floor(self.painter.getWindowHeightInTiles()/5), y)

    @repaintAfterOperation
    def right(self, event):
        x,y = self.painter.current_focus
        self.painter.current_focus = (x + math.floor(self.painter.getWindowHeightInTiles()/5), y)

    @repaintAfterOperation
    def setTileSize(self, size):
        self.painter.tile_size = size


class CanvasPainter(object):
    def __init__(self, canvas : tk.Canvas):
        self.image_list = [] #This is only here to deal with tkinter photoimage garbage-collection issue.
        #All created images MUST end up in image_list.
        self.canvas = canvas
        self.mode = world_state.ABOVE_GROUND
        #tile_size is both height and width of tiles (they're always square.)
        self.tile_size = 30
        #current_focus represents what the upper-leftmost tile's coordinates are.
        #all other tiles are drawn relative to it.
        self.current_focus = (0,0)



    def getWindowHeightInTiles(self):
        return math.floor(CANVAS_HEIGHT / self.tile_size)

    def drawTerrain(self, tile, x_coord, y_coord):
        terr = tile.terrain
        terrain_color = colors.rgbToHex(ter.NAME_TO_COLOR[terr])
        id = self.canvas.create_rectangle((x_coord, y_coord, self.tile_size + x_coord, self.tile_size + y_coord),
            fill=terrain_color, outline = "white")

    def drawRoads(self, tile : basic_map.Tile, x_coord, y_coord):
        has_road = tile.road
        if has_road is not None:
            center = x_coord + self.tile_size/2,y_coord + self.tile_size/2
            top = x_coord + self.tile_size/2, y_coord
            bot = x_coord + self.tile_size/2, y_coord + self.tile_size
            right = x_coord + self.tile_size, y_coord + self.tile_size/2
            left = x_coord, y_coord  + self.tile_size/2
            x = tile.x
            y = tile.y
            map = BOARD_STATE.map_dict[self.mode]
            if (map.getTile(x,y+1).road is not None):
                self.canvas.create_line(center, bot, fill = "brown")
            if (map.getTile(x,y-1).road is not None):
                self.canvas.create_line(center, top, fill = "brown")
            if (map.getTile(x+1, y).road is not None):
                self.canvas.create_line(center, right, fill = "brown")
            if (map.getTile(x-1,y).road is not None):
                self.canvas.create_line(center, left, fill = "brown")

        pass

    def drawCity(self, tile : basic_map.Tile, x, y):
        if tile.city is not None:
            city_image = tile.city.get_image(self.tile_size, self.tile_size)
            self.canvas.create_image(x, y, image = city_image, anchor = tk.NW)
            self.image_list.append(city_image) #Necessary to guard against garbage collection
        pass

    def drawTile(self, tile, x, y):
        current_map = BOARD_STATE.map_dict[self.mode]

        x_coord = x * self.tile_size
        y_coord = y * self.tile_size
        self.drawTerrain(tile, x_coord, y_coord)
        self.drawRoads(tile, x_coord, y_coord)
        self.drawCity(tile, x_coord, y_coord)


    def repaint(self):
        self.canvas.delete(tk.ALL)
        self.image_list = []
        current_map = BOARD_STATE.map_dict[self.mode]

        canvas_width = CANVAS_WIDTH
        canvas_height = CANVAS_HEIGHT
        num_tiles_x = math.floor(canvas_width / self.tile_size)
        num_tiles_y = math.floor(canvas_height / self.tile_size)

        start_tile_x, start_tile_y = self.current_focus
        tiles_to_draw = [(current_map.getTile(x,y),x - start_tile_x,y - start_tile_y) for x in range(start_tile_x, start_tile_x + num_tiles_x)
                         for y in range(start_tile_y, start_tile_y + num_tiles_y)]
        for tile in tiles_to_draw:
            self.drawTile(*tile)



#Actions list
PAINT_TERRAIN = 'paint'



class ViewContext(object):
    """
    This class is for collecting mouse events and doing appropriate things with them (as defined by self.action.)
    Self.action only knows about the tile being collected; the rest of the information is stored in the ViewContext.
    """
    def __init__(self, painter : CanvasPainter, map : world_state.WorldState):
        self.action = self.paintTerrain
        self.terrain = ter.DESERT
        self.painter = painter
        self.map = map

    def changeTerrain(self, name, index, mode):
        varValue = root.globalgetvar(name)
        self.terrain = varValue

    def clickOnCanvas(self, event):
        x,y = event.x, event.y
        x_tile = math.floor(x / self.painter.tile_size)
        y_tile = math.floor(y / self.painter.tile_size)
        dx, dy = self.painter.current_focus
        x_tile += dx
        y_tile += dy
        self.action(x_tile, y_tile)


    @repaintAfterOperation
    def paintTerrain(self, x_tile, y_tile):
        map = self.map.map_dict[self.painter.mode]
        map.tile_grid[x_tile][y_tile].terrain = self.terrain
        pass




if __name__ == '__main__':
    MainFrame()
