import surface_map
import basic_map
import cavern_map

__author__ = 'Aaron Kaufman'

ABOVE_GROUND = "above ground"
BELOW_GROUND = "below ground"

#Sort of a holder for all of the maps that one world has.
class WorldState(object):


    def __init__(self):
        self.size = 50
        self.map_dict = {ABOVE_GROUND : surface_map.SurfaceMap(self.size),
                         BELOW_GROUND : cavern_map.CavernMap(self.size)}

    def restart(self):
        for map in self.map_dict.values():
            map.remake()
            print("BAM")
