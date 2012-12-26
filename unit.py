__author__ = 'Aaron Kaufman'
from mapgen import MapGenerator
from basicmap import Tile


class Unit(object):
    def __init__(self,  chart:MapGenerator, pos:tuple, speed:int=200, direction:tuple=(0,0)):
        self.pos=pos
        self.speed = speed #moves every 200 ticks
        self.direction = direction
        self.objective_pos = None
        self.mapgen = chart

    def move(self):
        if (self.pos == self.objective_pos):
            objective_pos = self.chart.getNewObjective()




