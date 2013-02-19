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
        self.map_dict = {ABOVE_GROUND : surface_map.SurfaceMap(self.size),
                         BELOW_GROUND : cavern_map.CavernMap(self.size)}

    def restart(self):
        for map in self.map_dict.values():
            map.remake()
            print("BAM")


    #Save/load methods

    def saveToDatabase(self, user_name, map_name):
        serialized_string = pickle.dumps(self)
        con = sqlite3.connect("world_builder.db")
        cur = con.cursor()

