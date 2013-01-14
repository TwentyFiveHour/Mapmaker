import world_map
import basic_map
import cavern_map

__author__ = 'Aaron Kaufman'

ABOVE_GROUND = "above ground"
BELOW_GROUND = "below ground"

#Sort of a holder for all of the maps that one game has.  Does all the coordinating between them, too (To be implemented!).
class GameMap(object):


    def __init__(self):
        self.size = 20
        self.map_dict = {ABOVE_GROUND : world_map.WorldMap(self.size),
                         BELOW_GROUND : cavern_map.CavernMap(self.size)}

