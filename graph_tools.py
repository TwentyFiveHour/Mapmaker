
from collections import deque
import heapq
import math


def getMinimumSpanningTree(point_list : list):
    """
    #Figures out the minimum spanning tree for a set of points (or rather, things with an x and y attribute).
    #Returns a list of point pairs corresponding to the minimum spanning tree.
    #Uses naive distance calculations (not A*), so it's just n^2 with number of cities.
    """
    if len(point_list) < 2:
        return []

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




        

