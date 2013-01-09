__author__ = 'Aaron Kaufman'
import basic_map

DEAD = "dead"
ALIVE = "alive"



class CellularAutomataGenerator:
    def __init__(self,  b : list, s : list, initial_map : basic_map.TileMap = basic_map.TileMap(50,50),):

        self.b = b
        self.s = s
        self.initial_map = initial_map
        self.max_x = initial_map.max_x
        self.max_y = initial_map.max_y


    def run(self, num_turns = 1):
        """
        """
        self.runSimulation()

    def runSimulation(self):
        tiles = [ self.initial_map.getTile(x,y) for x in range (0, self.max_x) for y in range(0, self.max_y)]
        for tile in tiles:
            if self.getNumLivingNeighbors(tile) in self.s and tile._state == ALIVE:
                tile._next_state = ALIVE
            elif self.getNumLivingNeighbors(tile) in self.b and tile._state == DEAD:
                tile._next_state = ALIVE
            else:
                tile._next_state = DEAD
        for tile in tiles:
            tile._state = tile._next_state



    def getNumLivingNeighbors(self, tile : basic_map.Tile):
        nearby_tiles_modifier = [(0,1), (0,-1), (1,1), (1,-1), (1,0), (-1,0), (-1,-1), (-1,1)]

        nearby_tiles_coords = [(tile.x + dx, tile.y + dy) for (dx,dy) in nearby_tiles_modifier]

        num_living_tiles = len([self.initial_map.getTile(*yz) for yz in nearby_tiles_coords
                        if self.initial_map.getTile(*yz)._state == ALIVE])
        return num_living_tiles


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
            x_list = self.initial_map.xList[x]
            for y in x_list:
                p.join(str(y) + " : ")
            print(p)