import tkinter as tk
from tkinter import ttk
import game_map
import math
import terrain
import colors

CANVAS_WIDTH = 500
CANVAS_HEIGHT = 500

def main():
    root = tk.Tk()

    content = ttk.Frame(root)
    canvas = tk.Canvas(content, borderwidth=5, relief="sunken", width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
    namelbl = ttk.Label(content, text="Name")
    name = ttk.Entry(content)
    content.grid(column = 0, row = 0)
    canvas.grid(column = 0, row = 0, columnspan = 10, rowspan = 10)
    info_frame = ttk.Frame(content,borderwidth = 5, width = 200, height = 500)
    info_frame.grid(column = 11, row = 0, columnspan = 3, rowspan = 9)

    view_level = tk.StringVar()


    label = ttk.Label(info_frame, text='Full name:')
    resultsContents = tk.StringVar()
    label['textvariable'] = resultsContents
    resultsContents.set('View Type')

    above_ground = ttk.Radiobutton(info_frame, text='Above Ground', variable=view_level, value=game_map.ABOVE_GROUND)
    below_ground = ttk.Radiobutton(info_frame, text='Under Ground', variable=view_level, value=game_map.BELOW_GROUND)
    view_level.set(game_map.ABOVE_GROUND)

    label.grid(column = 11,row=0)
    above_ground.grid(column = 11, row = 1)
    below_ground.grid(column = 11, row = 2)

    painter = CanvasPainter(canvas, game_map.GameMap())
    painter.repaint()

    root.mainloop()


class CanvasPainter(object):



    def __init__(self, canvas : tk.Canvas, map : game_map.GameMap):
        self.canvas = canvas
        self.mode = game_map.ABOVE_GROUND
        self.game_map = map
        #tile_size is both height and width of tiles (they're always square.)
        self.tile_size = 30
        #current_focus represents what the upper-leftmost tile's coordinates are.
        #all other tiles are drawn relative to it.
        self.current_focus = (0,0)

    def drawTerrain(self, tile, x_coord, y_coord):
        terr = tile.terrain
        terrain_color = colors.rgbToHex(terrain.NAME_TO_COLOR[terr])
        id = self.canvas.create_rectangle((x_coord, y_coord, self.tile_size, self.tile_size),
            fill=terrain_color, tags=('palette', 'palettered'))

    def drawTile(self, tile):
        current_map = self.game_map.map_dict[self.mode]
        num_tiles_x = math.floor(CANVAS_WIDTH / self.tile_size)
        num_tiles_y = math.floor(CANVAS_HEIGHT / self.tile_size)
        start_tile_x, start_tile_y = self.current_focus

        x_coord = (tile.x - start_tile_x) * self.tile_size
        y_coord = tile.y - start_tile_y * self.tile_size

        self.drawTerrain(tile, x_coord, y_coord)


    def repaint(self):
        #Checks what map we're currently displaying.
        current_map = self.game_map.map_dict[self.mode]
        canvas_width = CANVAS_WIDTH
        canvas_height = CANVAS_HEIGHT
        num_tiles_x = math.floor(canvas_width / self.tile_size)
        num_tiles_y = math.floor(canvas_height / self.tile_size)

        start_tile_x, start_tile_y = self.current_focus
        tiles_to_draw = [current_map.getTile(x,y) for x in range(start_tile_x, start_tile_x + num_tiles_x)
                         for y in range(start_tile_y, start_tile_y + num_tiles_y)]
        for tile in tiles_to_draw:
            self.drawTile(tile)



if __name__ == '__main__':
    main()
