import city
import terrain as ter
import perlin_noise
import utils

class Tile(object):
    '''
    classdocs
    This represents a tile.
    Tiles have an associated Continent and an associated TerrainType.
    '''


    def __init__(self, terrain, x, y):
        '''
        Constructor
        '''

        self.terrain = terrain
        self.x = x
        self.y = y
        self.height = 0
        self.sort_key = 0
        self.road = None
        self.city = None
        self.map_transition = None


        assert(self.city is city.City or self.city is None)
    def __str__(self):
        if self.city is  not None:
            return self.city
        else:
            return self.terrain
    def __repr__(self):
        return ("[Terrain: "+self.terrain+" coords : " + str(self.x) + ", " + str(self.y) + "]")


    def getProperty(self, property_name):
        return self.__getattribute__(property_name)

    def getSortKey(self):
        return self.sort_key






class TileMap(object):



    def __init__(self, max_x, max_y):
        self.max_x = max_x
        self.max_y = max_y
        self.wrap_x = True
        self.wrap_y = True
        self.IMPASSIBLE_TILE = Tile(ter.IMPASSIBLE, -1, -1)
        self.tile_grid = []
        for x in range(0, self.max_x):
            yList = []
            self.tile_grid.append(yList)
            for y in range(0, self.max_y):
                 yList.append(Tile(ter.WATER, x, y))

    #Benchmark: 11.3 with checks.
    def getTile(self, x, y) -> Tile:
        if (self.wrap_x and not (0 <= x < self.max_x)):
            x = utils.modu(x, self.max_x)
        if (self.wrap_y and not (0 <= y < self.max_y)):
            y = utils.modu(y, self.max_y)

        if not (0<=x<self.max_x):
            return self.IMPASSIBLE_TILE
        if not (0<=y<self.max_y):
            return self.IMPASSIBLE_TILE
        return self.tile_grid[x][y]


    def makePropertiedHeightMap(self, the_property, smoothness, bias = None, bias_amplitude = None):
        """
        #This is a method to create a height map on the tilemap with any property,
        # using perlin noise.
        #(Ex: the_property can be "height", "temperature", or anything else.)
        #This new property is placed into the attributes of each tile with the new value.
        #"Smoothness" defines how many tiles exist between two perlin noise spikes.
        "Bias" refers to a function that can modify the resulting height according to the tile's spatial location.
        "Bias_amplitude" refers to how much of an impact this will have on the resulting heightmap.

        """

        gen = self.buildPerlinNoiseGenerator(smoothness)

        tiles_list = [self.getTile(x,y) for x in range(0,self.max_x) for y in range(0, self.max_y)]
        for tile in tiles_list:
            x = tile.x
            y = tile.y

            p_x = x/smoothness
            p_y = y/smoothness

            #            if (self.wrap_x):
            #               p_x = utils.modu(p_x, grid_size_x)
            #          if (self.wrap_y):
            #             p_y = utils.modu(p_y, grid_size_y)
            bias_value = 0
            if bias is not None:
                assert(bias_amplitude is not None)
                bias_value = bias(self, tile, bias_amplitude)
            else:
                assert(bias_amplitude is None)
            value = gen.interpolate(p_x,p_y) + bias_value
            tile.__setattr__(the_property, value)



    def buildPerlinNoiseGenerator(self, smoothness) -> perlin_noise.perlinNoiseGenerator:
        """
        Creates a perlin noise generator fitting the requirements of this world map.
        """
        grid_size_x = self.max_x/smoothness
        grid_size_y = self.max_y/smoothness
        if (grid_size_x < 1):
            grid_size_x = 1
        if (grid_size_y < 1):
            grid_size_y = 1

        gen = perlin_noise.perlinNoiseGenerator()
        gen.wrap_x = grid_size_x
        gen.wrap_y = grid_size_y
        return gen

    def declareEffectiveProperties(self, property_name, percentile_to_title, title_name):
        """
        #Maps out the property given to a percentile.
        #percentile_to_title is a dictionary
        #Ex:  99 percentile covers the top 99% of the map.
        #title refers to the name of the property given to the tile.
        #property refers to the field that the title is derived from.
        For example, the property could be temperature, and that could correspond to the titles ("title_name")
        "warm", "cold", or "medium" depending on percentile.
        """
        flattened_tile_list = [self.getTile(x,y) for x in range(0, self.max_x) for y in range(0, self.max_y)]
        for tile in flattened_tile_list:

            tile.sort_key = tile.__getattribute__(property_name)

        key_list = percentile_to_title.keys()
        key_list = sorted(key_list)

        flattened_tile_list.sort(key = Tile.getSortKey, reverse = False)
        current = 0
        for tile in flattened_tile_list:
            if len(key_list)==0:
                return
            current+=1
            current_percent_finished = current/len(flattened_tile_list)*100
            if (key_list[0] < current_percent_finished):
                key_list.pop(0)    #If we've finished with the current key, chuck it from the stack!
            tile.__setattr__(title_name, percentile_to_title.get(key_list[0]))


    def __str__(self):
        temp = ''
        for x in range(self.max_x):
            for y in range(self.max_y):
                temp = temp + str(self.getTile(x, y))
            temp = temp + '\n'
        return temp

    def getAllTiles(self):
        return [self.getTile(x,y)
                for x in range (0, self.max_x)
                for y in range(0, self.max_y)]


    def remake(self):
        """
        Implicit guarantee that all map implementations have some version of "remake"
        For compiler hints.
        """
        return

    def getNearbyTiles(self, tile):
        """
        Gets all four tiles near the given tile,
        plus a seed tile from the map if there are any map transitions.
        """
        returned = []
        if (0 < tile.x < self.max_x - 2 and 0 < tile.y < self.max_y - 2): #check that we're not on boundary
            returned = [self.tile_grid[x][y] for x,y in utils.NEARBY_TILE_COORDS]
        else:   # This call is much more expensive.
            returned = [self.getTile(x,y) for x,y in utils.NEARBY_TILE_COORDS]
        if (tile.map_transition is not None):
            returned.append(tile.map_transition.getTile(tile.x,tile.y))
        return returned
