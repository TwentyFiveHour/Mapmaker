import surface_map
import basic_map
import cavern_map
import pickle
import sqlite3

__author__ = 'Aaron Kaufman'

ABOVE_GROUND = "above ground"
BELOW_GROUND = "below ground"

INSERT_MAP_QUERY = "insert into t_maps (user_id, map_name, serialized_map) " \
                     "VALUES (?, (select user_id from t_users where user_name = ?)  ,?, ?)"


#Sort of a holder for all of the maps that one world has.
class WorldState(object):


    def __init__(self):
        self.size = 50
        self.map_dict = {ABOVE_GROUND : surface_map.SurfaceMap(self.size, self.size),
                         BELOW_GROUND : cavern_map.CavernMap(self.size, self.size)}

    def restart(self, x = 50, y = 50, polar_bias = 1, island_bias = 1, percent_water = surface_map.PERCENT_WATER):
        self.map_dict[ABOVE_GROUND] = surface_map.SurfaceMap(x,y)
        self.map_dict[ABOVE_GROUND].polar_bias = surface_map.POLAR_BIAS * polar_bias
        self.map_dict[ABOVE_GROUND].island_bias = surface_map.ISLAND_BIAS * island_bias
        self.map_dict[ABOVE_GROUND].percent_water = percent_water

        self.map_dict[BELOW_GROUND] = cavern_map.CavernMap(x,y)

        for m in self.map_dict:
            self.map_dict[m].remake()

