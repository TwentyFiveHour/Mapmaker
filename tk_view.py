import tkinter as tk
from tkinter import ttk
import world_state
import math
import terrain
import colors
import basic_map
import utils
from tkinter import messagebox

CANVAS_WIDTH = 500
CANVAS_HEIGHT = 500

BOARD_STATE = world_state.WorldState()



def repaintAfterOperation(f):
    def wrapper(self, *args):
        return_val = f(self, *args)
        self.painter.repaint()
        return return_val
    return wrapper

class MainFrame(object):
    def __init__(self):

        root = tk.Tk()
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
        self.content = content
        label = ttk.Label(info_frame, text='Full name:')
        resultsContents = tk.StringVar()
        label['textvariable'] = resultsContents
        resultsContents.set('View Type')

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
        self.painter.current_focus = (x, y + 2)

    @repaintAfterOperation
    def up(self, event):
        x,y = self.painter.current_focus
        self.painter.current_focus = (x, y - 2)

    @repaintAfterOperation
    def left(self, event):
        x,y = self.painter.current_focus
        self.painter.current_focus = (x - 2, y)

    @repaintAfterOperation
    def right(self, event):
        x,y = self.painter.current_focus
        self.painter.current_focus = (x + 2, y)

    @repaintAfterOperation
    def setTileSize(self, size):
        self.painter.tile_size = size


class CanvasPainter(object):
    def __init__(self, canvas : tk.Canvas):
        self.canvas = canvas
        self.mode = world_state.ABOVE_GROUND
        #tile_size is both height and width of tiles (they're always square.)
        self.tile_size = 30
        #current_focus represents what the upper-leftmost tile's coordinates are.
        #all other tiles are drawn relative to it.
        self.current_focus = (0,0)

    def drawTerrain(self, tile, x_coord, y_coord):
        terr = tile.terrain
        terrain_color = colors.rgbToHex(terrain.NAME_TO_COLOR[terr])
        id = self.canvas.create_rectangle((x_coord, y_coord, self.tile_size + x_coord, self.tile_size + y_coord),
            fill=terrain_color, outline = "white")


    def drawTile(self, tile, x, y):
        current_map = BOARD_STATE.map_dict[self.mode]

        x_coord = x * self.tile_size
        y_coord = y * self.tile_size

        self.drawTerrain(tile, x_coord, y_coord)

    def repaint(self):
        self.canvas.delete(tk.ALL)
        current_map = BOARD_STATE.map_dict[self.mode]
        print("REPAINTING")

        canvas_width = CANVAS_WIDTH
        canvas_height = CANVAS_HEIGHT
        num_tiles_x = math.floor(canvas_width / self.tile_size)
        num_tiles_y = math.floor(canvas_height / self.tile_size)

        start_tile_x, start_tile_y = self.current_focus
        tiles_to_draw = [(current_map.getTile(x,y),x - start_tile_x,y - start_tile_y) for x in range(start_tile_x, start_tile_x + num_tiles_x)
                         for y in range(start_tile_y, start_tile_y + num_tiles_y)]
        for tile in tiles_to_draw:
            self.drawTile(*tile)


if __name__ == '__main__':
    MainFrame()
