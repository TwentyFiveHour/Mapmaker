__author__ = 'Aaron Kaufman'

import perlin_noise
import random
import math

if __name__ == '__main__':


    gen = perlin_noise.perlinNoiseGenerator()
    a = gen.noise2d(2,3)
    b = gen.noise2d(2,3)

    c = gen.noise2d(3,2)
    assert(a==b)
    assert(a!=c)

    gen2 = perlin_noise.perlinNoiseGenerator()
    assert(gen2.noise2d(3,3) != gen.noise2d(3,3))
    point = 1,1.4

    this_one = gen.interpolate(*point)
    that_one = gen.interpolate(*point)

    a_different_one = gen.interpolate(30,8.3)
    assert(this_one == that_one)
    assert(this_one != a_different_one)

    a_mid_point = 30.5,30.5
    x,y=a_mid_point
    a = math.floor(x),math.floor(y)
    b = math.floor(x),math.ceil(y)
    c = math.ceil(x), math.floor(y)
    d = math.ceil(x), math.ceil(y)

    outer_points = a,b,c,d
    noise = [gen.noise2d(x,y) for x,y in outer_points]
    average = sum(noise)/float(len(noise))
    calculated = gen.interpolate(30.5,30.5)
    #Algorithm requires that a point midway between all nearest vertices have a height equal to that
    #of all points.
    assert(math.fabs(average - calculated) < 0.001)

    rounded_point = 30,30
    #Checks that the noise generated for that point is the same as the interpolated value for that point.
    assert(gen.interpolate(*rounded_point) == gen.noise2d(*rounded_point))

