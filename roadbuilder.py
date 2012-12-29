
from basicmap import Tile
import basicmap as bmap
from collections import deque
import heapq
import math
PASSABLE_DICT = {"mountain" : False,
                 "water" : False}

def getPassable(t:Tile):
    return PASSABLE_DICT.setdefault(t.terrain, True)


def findJoinableCitySets(map: bmap.TileMap):
    """
    #returns a set of cities connected to each other by passable terrain
    """
    
    city_tile_set = [map.getTile(x,y) for x in range(0, map.max_x) for y in range(0,map.max_y)
                     if map.getTile(x,y).city is not None]
    full_tile_set = [map.getTile(x,y) for x in range(0,map.max_x) for y in range(0,map.max_y)]
    for tile in full_tile_set:
        tile._has_been_visited = False
    previously_encountered_city_tiles = []
    contiguous_city_list_list = []
    for city_tile in city_tile_set:
        if city_tile in previously_encountered_city_tiles:
            continue
        #tracks contiguous tiles found for this city_tile_set.
        #open_set acts as a queue.
        cont_cities = [] #This is what we'll be "returning" from the loop: each list of contiguous city tiles goes
        #into the cont_cities list.
        open_set = deque()
        open_set.appendleft(city_tile)
        while (open_set):
            t = open_set.pop()
            x=t.x
            y=t.y
            if not getPassable(t):  #don't use this tile if we can't pass it.
                continue
            if (True is t._has_been_visited): # don't use this tile if it has been visited.
                continue
            else:
                if (t in open_set):
                    continue
                t._has_been_visited = True
                n = map.getTile(x,y+1)
                s = map.getTile(x,y-1)
                e = map.getTile(x+1,y)
                w = map.getTile(x-1,y)
                addTileIfAdmissible(open_set, n)
                addTileIfAdmissible(open_set, s)
                addTileIfAdmissible(open_set, e)
                addTileIfAdmissible(open_set, w)
                if (t.city is not None):
                    cont_cities.append(t)
                    previously_encountered_city_tiles.append(t)
        contiguous_city_list_list.append(cont_cities)
    return contiguous_city_list_list


def addTileIfAdmissible(deq:deque, t:Tile):
    if (getPassable(t) and not t._has_been_visited):
        if t not in deq:
            deq.appendleft(t)



class Node(object):
    """
    #heuristic refers to linear distance to goal node.
    #The first node should have a parent of None.
    #Parent is the node this node was spawned off of; used for ancestry.
    """
    def __init__(self, tile : Tile, parent, heuristic):
        self.tile = tile
        self.parent = parent
        self.heuristic = heuristic
        if parent is not None:
            self.distance = parent.distance + 1
        else:
            self.distance = 0


    def getAncestry(self) -> list:
        nodes = []
        current = self
        while current is not None:
            nodes.append(current.tile)
            current = current.parent
        return nodes

    def __lt__(node1,node2):

        return (node1.heuristic + node1.distance) < (node2.heuristic + node2.distance)



class AStarNodeMap(object):
    """
    #Represents the A-Star algorithm on a tiled map
    """
    def __init__(self, map : bmap.TileMap, start:Tile, goal:Tile):

        self.start = start
        self.already_hit = []
        self.open_set = []
        heapq.heapify(self.open_set)
        heapq.heappush(self.open_set, Node(start, None, 1))
        self.goal = goal
        self.map = map

    def getLinearDistanceToGoal(self, x, y) -> int:
        """

        #Acts as heuristic for A-star algorithm.  Gets distance between given point and the goal.
        """
        dx2 = pow(x - self.goal.x, 2)
        dy2 = pow(y - self.goal.y, 2)
        return math.sqrt(dx2 + dy2)


    def buildAdjacentNodes(self, parent:Node):
        """
        Builds nodes adjacent to the current tile if the current tile is "valid", and adds them to the open set.
        """
        x = parent.tile.x
        y = parent.tile.y
        n = self.map.getTile(x,y+1)
        s = self.map.getTile(x,y-1)
        e = self.map.getTile(x+1,y)
        w = self.map.getTile(x-1,y)

        new_tiles = [n,s,e,w]
        for tile in new_tiles:
            if ((tile.x,tile.y) not in self.already_hit and getPassable(tile)):
                heapq.heappush(self.open_set, Node(tile, parent, self.getLinearDistanceToGoal(tile.x, tile.y)))
                tup = (tile.x, tile.y)
                self.already_hit.append(tup)


    def getAStarResult(self) -> list:
        current = Node(self.start, None, 0)
        while current.tile is not self.goal:
            current = heapq.heappop(self.open_set)
            self.buildAdjacentNodes(current)
        return current.getAncestry()


