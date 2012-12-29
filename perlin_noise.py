#Author:  Aaron Kaufman
import random
import math
import utils
from utils import memo
import functools
class perlinNoiseGenerator(object):




    def __init__(self, amplitude : tuple = (0,100), wrap_x : int = -1, wrap_y : int = -1, seed = None):
        """
        #Size tuple refers to the number of points directly created by the noise function in the X and Y directions,
        #respectively.
        #Amplitude determines the variance in numbers.
        #seed determines a specific random seed.
        #wrap defines after how many points the heightmap starts repeating.
        """
        if seed is None:
            self.seed = random.random()
        else:
            self.seed = seed
        self.wrap_x = wrap_x
        self.wrap_y = wrap_y


        self.lower_bound, self.upper_bound = amplitude



    @memo
    def noise2d(self, x : int, y : int, bias = 0):
        """
        #Note: If random seed changes, we have an ENTIRELY new map.
        #Gets our noise function for a given coordinate.  MUST be an integer.
        #Returns the same random number for the same coordinates regardless of how many times it's called.
        #Returns a result that is between the lower and upper bounds of the amplitude.
        """

        if (self.wrap_x > 0):
            x = utils.modu(x, self.wrap_x)
        if (self.wrap_y > 0):
            y = utils.modu(y, self.wrap_y)

        random.seed('' + str(x) + 'x' + str(y) + 'y' + str(self.seed))
        return random.random()* (self.upper_bound-self.lower_bound) + self.lower_bound

    def generateNewSeed(self):
        self.seed = random.random


    def interpolate(self, x : float, y : float):
        """
        #Finds the nearest four coordinates to the selected point, and interpolates between them returning
        #their weighted average.
        """
        floor_x = math.floor(x)
        floor_y = math.floor(y)
        ceil_x = math.ceil(x)
        ceil_y = math.ceil(y)

        a = (floor_x, floor_y)
        b = (ceil_x, floor_y)

        c = (floor_x, ceil_y)
        d = (ceil_x, ceil_y)


        ease_x = self.easeFunction(ceil_x - x)
        ease_y = self.easeFunction(ceil_y - y)

        noise_top_1 = ease_x * self.noise2d(*c)
        noise_top_2 = (1-ease_x) * self.noise2d(*d)
        noise_top = noise_top_1 + noise_top_2
        noise_bot_1 =  ease_x * self.noise2d(*a)
        noise_bot_2 = (1-ease_x) * self.noise2d(*b)
        noise_bot = noise_bot_1 + noise_bot_2

        noise_average = noise_top * (1-ease_y) + noise_bot * (ease_y)

        return noise_average








    def easeFunction(self, num : float):
        """
        #USAGE:  Feed it a number between 0 and 1, and it will output a number between lower_bound and upper_bound
        #that's a weighted average between them.
        """
        if (num > 1 or num < 0):
            raise AssertionError("ERROR:  Ease function can only accept arguments between zero and one.")
        return (3 * math.pow(num,2) - 2 * math.pow(num,3))


