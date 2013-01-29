__author__ = 'Aaron Kaufman'
import basic_map
import random
import math

DEAD = "dead"
ALIVE = "alive"



NEARBY_TILE_COORDS= [(0,1), (0,-1), (1,1), (1,-1), (1,0), (-1,0), (-1,-1), (-1,1)]

class CellularAutomataGenerator:
    def __init__(self,  b : list, s : list, initial_map : basic_map.TileMap = basic_map.TileMap(50,50),):

        self.b = b
        self.s = s
        self.initial_map = initial_map
        self.initial_map.IMPASSIBLE_TILE._state = DEAD #If we're not wrapping, treat the impassible tile as dead. (If we are, we'll never see it.)
        self.max_x = initial_map.max_x
        self.max_y = initial_map.max_y
        self.clearSimulation(DEAD)




    def run(self, num_turns = 1):
        """
        Runs the simulation for num_turns number of turns.
        Note: The inner loop looks a bit wonky because the cleaner-looking method
        of using getTile() to take advantage of wrapping
        """
        map = self.initial_map
        tiles = [ map.tile_grid[x][y] for x in range (0, self.max_x) for y in range(0, self.max_y) ]
        for _ in range(0,num_turns):
            for tile in tiles:
                x = tile.x
                y = tile.y
                nearby_tiles_coords = []
                if (0 < x < self.max_x - 1 and 0 < y < self.max_y - 1): #If we're not at a boundary, do cheap computation.
                    nearby_tiles_coords = [(x + dx, y + dy) for (dx,dy) in NEARBY_TILE_COORDS]
                    num_living_tiles = len([map.tile_grid[x][y] for x,y in nearby_tiles_coords
                                            if map.tile_grid[x][y]._state == ALIVE ])
                else: #If we're at a boundary, do the expensive computation.
                    nearby_tiles_coords = [(x + dx, y + dy) for (dx,dy) in NEARBY_TILE_COORDS]
                    num_living_tiles = len([self.initial_map.getTile(x,y) for x,y in nearby_tiles_coords
                                            if self.initial_map.getTile(x,y)._state == ALIVE])

                if num_living_tiles in self.s and tile._state == ALIVE:
                    tile._next_state = ALIVE
                elif num_living_tiles in self.b and tile._state == DEAD:
                    tile._next_state = ALIVE
                else:
                    tile._next_state = DEAD
            for tile in tiles:
                tile._state = tile._next_state




    def clearSimulation(self, state : str):
        for tile in [self.initial_map.getTile(x,y)
                     for x in range (0, self.initial_map.max_x)
                     for y in range(0, self.initial_map.max_y)]:
            tile._state = state

    def finalizeMap(self, state_to_terrain_dict):
        alive_ter = state_to_terrain_dict[ALIVE]
        dead_ter = state_to_terrain_dict[DEAD]

        for tile in [self.initial_map.getTile(x,y)
                     for x in range (0, self.initial_map.max_x)
                     for y in range(0, self.initial_map.max_y)]:
            tile.terrain = state_to_terrain_dict[tile._state]

    def printSimulation(self):
        """
        Prints a representation of the final map to console.
        """
        for x in range(0, self.initial_map.max_x):
            p = ""
            x_list = self.initial_map.tile_grid[x]
            for y in x_list:
                p.join(str(y) + " : ")
            print(p)


    def randomizeInitialConditions(self, fraction_alive):
        """
        fraction_alive: a number between 0 and 1, 1 indicating that all cells are alive,
        and 0 indicating that all cells are dead.
        """
        num_tiles = math.floor(self.max_x * self.max_y * fraction_alive)
        all_tiles = self.initial_map.getAllTiles()


        for _ in range(0,num_tiles):
            current = random.choice(all_tiles)
            all_tiles.remove(current)
            current._state = ALIVE

