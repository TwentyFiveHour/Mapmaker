__author__ = 'Aaron Kaufman'

import functools
import math


def getLinearDistanceSquared(start_point, end_point, max_x : int, max_y : int, x_wrap : bool, y_wrap : bool):
    """
    start_point and end_point are basically anything with an x and y property.
    """
    x1,y1 = start_point.x, start_point.y
    x2,y2 = end_point.x, end_point.y

    dx = math.fabs(x1-x2)
    dy = math.fabs(y1-y2)

    if (dx > max_x/2 and x_wrap):
        x1 = modu(x1 + max_x/2, max_x)
        x2 = modu(x2 + max_x/2, max_x)
    if (dy > max_y/2 and y_wrap):
        y1 = modu(y1 + max_y/2, max_y)
        y2 = modu(y2 + max_y/2, max_y)

    dx2 = pow(x1 - x2, 2)
    dy2 = pow(y1 - y2, 2)
    return dx2 + dy2

def getLinearDistance(start_point, end_point, max_x, max_y, x_wrap, y_wrap):
    return math.sqrt(getLinearDistanceSquared(start_point, end_point, max_x, max_y, x_wrap, y_wrap))



#re-implements modulo operator such that it always returns a positive remainder(used for wrapping)
def modu(num, divby):
    return (num % divby + abs(divby))%divby

#Stolen shamelessly from some other python library
def memo(func):
    cache = {}
    @ functools.wraps(func)
    def wrap(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrap

NEARBY_TILE_COORDS_INCLUDING_DIAGONALS= [(0,1), (0,-1), (1,1), (1,-1), (1,0), (-1,0), (-1,-1), (-1,1)]
NEARBY_TILE_COORDS = [(0,1),(1,0),(-1,0),(0,-1)]