import city
import terrain as ter

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

        self.road = None
        self.terrain = terrain
        self.x = x
        self.y = y
        self.height = 0
        self.sort_key = 0
        self.city = None
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
        self.xList = []
        for x in range(0, self.max_x):
            yList = []
            self.xList.append(yList)
            for y in range(0, self.max_y):
                 yList.append(Tile(ter.WATER, x, y))