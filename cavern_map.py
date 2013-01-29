import basic_map
import cellular_automata as ca
import cProfile
import terrain

B = [5,6,7,8,9]
S = [4,5,6,7,8,9]
BASE_WALL_PROBABILITY = .5




class CavernMap( basic_map.TileMap):

    def __init__(self, max_x = 50, max_y =50):
        basic_map.TileMap.__init__(self, max_x, max_y)

    def remake(self):
        gen = ca.CellularAutomataGenerator(B,S,self)
        gen.randomizeInitialConditions(BASE_WALL_PROBABILITY)
        gen.run(15)
        gen.finalizeMap({ca.ALIVE : terrain.PLAINS, ca.DEAD : terrain.MOUNTAIN})

if __name__ == '__main__':
    cProfile.run('CavernMap(50,50)')