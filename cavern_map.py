import basic_map
import cellular_automata as ca

B = [5,6,7,8,9]
S = [4,5,6,7,8,9]
BASE_WALL_PROBABILITY = .45

class CavernMap( basic_map.TileMap):

    def __init__(self, max_x = 50, max_y =50):
        basic_map.TileMap.__init__(self, max_x, max_y)
        gen = ca.CellularAutomataGenerator(B,S,self)
        gen.randomizeInitialConditions(BASE_WALL_PROBABILITY)
        gen.run(15)



