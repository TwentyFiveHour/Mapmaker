__author__ = 'Aaron Kaufman'
import mapgen
import basicmap
import roadbuilder
#Python unit test!

if __name__ == '__main__':
    #FIRST:  Contiguous city tile test.
    #Question asked: Does our algorithm properly determine what cities are connectable?

    map = mapgen.MapGenerator(4,4)
    map.clearAllTerrain('water')
    map.getTile(0,0).terrain = 'grass'
    map.getTile(0,1).terrain = 'grass'
    map.getTile(0,2).terrain = 'grass'

    A = map.getTile(0,2)
    B = map.getTile(0,0)
    A.city = "A"
    B.city = "B"

    map.getTile(2,2).terrain = 'grass'
    map.getTile(2,2).city = "C"
    #TODO: Replace with assertion\

    lis = roadbuilder.findJoinableCitySets(map)
    num_groups = 0
    while (lis):
        cur = lis.pop()
        if (len(cur) == 2):  #There needs to be one list of length two containing A and B.
            t = cur.pop()
            num_groups+=1
            assert t.city == 'A' or t.city == 'B', "Got wrong list: %s" %cur
        elif (len(cur) == 1):
            t = cur.pop()
            assert t.city == 'C', "Got wrong list: %s" %cur  #There needs to be one list of length one containing C.
            num_groups+=1

    assert(num_groups == 2)

    #Now, a test of the AStarNodeMap.

    astar = roadbuilder.AStarNodeMap(map, A, B)
    result = astar.getAStarResult()
    assert result[0] == B
    assert result[1].terrain == 'grass'
    assert result[2] == A



