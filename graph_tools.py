
from basicmap import Tile
import basicmap as bmap
from collections import deque
import heapq
import math
PASSABLE_DICT = {"mountain" : False,
                 "water" : False}

def _getPassable(t:Tile):
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
            if not _getPassable(t):  #don't use this tile if we can't pass it.
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
                _addTileIfAdmissible(open_set, n)
                _addTileIfAdmissible(open_set, s)
                _addTileIfAdmissible(open_set, e)
                _addTileIfAdmissible(open_set, w)
                if (t.city is not None):
                    cont_cities.append(t)
                    previously_encountered_city_tiles.append(t)
        contiguous_city_list_list.append(cont_cities)
    return contiguous_city_list_list


def _addTileIfAdmissible(deq:deque, t:Tile):
    if (_getPassable(t) and not t._has_been_visited):
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



class _AStarNodeMap(object):
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
            if ((tile.x,tile.y) not in self.already_hit and _getPassable(tile)):
                heapq.heappush(self.open_set, Node(tile, parent, self.getLinearDistanceToGoal(tile.x, tile.y)))
                tup = (tile.x, tile.y)
                self.already_hit.append(tup)


    def getAStarResult(self) -> list:
        current = Node(self.start, None, 0)
        while current.tile is not self.goal:
            current = heapq.heappop(self.open_set)
            self.buildAdjacentNodes(current)
        return current.getAncestry()

def getClosestRoute(map : bmap.TileMap, start:Tile, goal:Tile):
    """
    Creates an A* node map and retrieves the result.
    """
    node_map = _AStarNodeMap(map,start,goal)
    return node_map.getAStarResult()


def getMinimumSpanningTree(point_list : list):
    """
    #Figures out the minimum spanning tree for a set of points (or rather, things with an x and y attribute).
    #Returns a list of point pairs corresponding to the minimum spanning tree.
    #Uses naive distance calculations (not A*), so it's just n^2 with number of cities.
    """

    point_pair_list = [(a,b) for a in point_list for b in point_list]
    primary_distance_dict = {}
    for point_pair in point_pair_list:
        a,b = point_pair
        distance_squared = math.pow(a.x-b.x, 2) + math.pow(a.y-b.y,2)
        primary_distance_dict[point_pair] = distance_squared


    sorted_pairs = sorted(primary_distance_dict, key=primary_distance_dict.get)
    sorted_pairs = [pair for pair in sorted_pairs if pair[0] is not pair[1]]
    spanning_tree = [sorted_pairs[0]]
    points_in_spanning_tree = set()
    #TODO:  pair[1] is a single thing, but we need tuples to compare w spanning_tree.
    points_in_spanning_tree.add((sorted_pairs[0][0]))
    points_in_spanning_tree.add((sorted_pairs[0][1]))
    distance_dict = dict([(pair, primary_distance_dict[pair]) for pair in primary_distance_dict.keys()
                              if pair[0] not in points_in_spanning_tree
                                and pair[1] in points_in_spanning_tree
                                and pair[1] is not pair[0]])
    while (distance_dict):
        next_pair = [pair for pair in distance_dict.keys()
                    if distance_dict[pair] == min(distance_dict.values())][0]
        spanning_tree.append(next_pair)
        points_in_spanning_tree.add((next_pair[0]))
        points_in_spanning_tree.add((next_pair[1]))
        new_distance_dict = dict([(pair, primary_distance_dict[pair]) for pair in primary_distance_dict.keys()
                if pair[0] not in points_in_spanning_tree
                and pair[1] in points_in_spanning_tree])
        distance_dict = new_distance_dict
    return spanning_tree




        

