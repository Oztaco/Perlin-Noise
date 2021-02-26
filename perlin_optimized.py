import pandas as pd
import math as m
from timing import timing
from collections import defaultdict

class Perlin:

    p = pd.Series()
    permutation = pd.Series()
    repeat = -1

    def __init__(self):

        self.p = [None] * 512  # Used as a hash function to determine gradient vectors

        # Hash lookup table - randomly arranged array of all numbers from 0-255 inclusive
        # Defined by Ken Perlin

        # This is the table used to define the gradient vectors, ie. the vectors at the edge of
        # each rectangle overlaying the noise which are then dotted with the distance vectors
        # to determine the value of any given coordinate
        #
        # Note: gradient vectors -> vectors going outside of overlayed grid
        #       distance vectors -> vecors defining the distance from any corner point on the overlayed
        #                           grid to any coordinate inside of it
        #
        # https://gamedev.stackexchange.com/questions/170239/understanding-the-gradient-in-perlin-noise#
        #
        permutation_lst = \
            [151,160, 137,91,90,15,131, 13,201,95,96,53, 194,233,7,225,140,36,
            103,30,69,142,8,99,37,240,21,10,23,190, 6,148,247,120,234,75,0,26,197,62,94,
            252,219,203, 117,35,11,32,57,177,33,88,237,149,56,87,174,20,125,136,171,168,
            68,175,74,165,71,134,139,48,27,166,77,146,158,231,83,111,229,122,60,211,133,
            230,220,105,92,41,55,46,245,40,244,102,143,54, 65,25,63,161,1,216,80,73,209,
            76,132,187,208, 89,18,169, 200,196, 135,130,116,188,159, 86,164,100,109,198,
            173,186, 3,64,52,217,226,250,124,123,5,202,38,147,118,126,255,82,85,212,207,
            206,59,227,47,16,58,17,182,189,28,42, 223,183,170,213,119, 248,152,2,44,154,
            163,70,221,153,101,155, 167,43,172,9,129,22,39,253,19,98,108,110,79,113,224,
            232,178,185, 112,104,218, 246,97,228,251, 34,242,193,238,210,144,12,191,179,
            162, 241,81,51,145,235,249,14,239,107,49,192, 214,31,181,199,106,157,184,84,
            204,176,115,121,50,45, 127,4,150,254,138,236,205,93,222,114,67,29,24,72,243,
            141,128,195,78,66,215,61,156,180]
        self.permutation = pd.Series(permutation_lst)
        
        # Populate p hash table.
        for i in range(512):
            self.p[i] = self.permutation[i % 256]


    def perlin(self, x:float, y:float, z:float) -> float:
        if (self.repeat > 0):
            # Localize coordinates inside of unit cube only in the case of repetition
            x = x % self.repeat
            y = y % self.repeat
            z = z % self.repeat

        # Calculate the "unit cube" in which the coordinates are located. The left
        # bound is ( |_x_|,|_y_|,|_z_| ) and the right bound is that plus 1. Ensure
        # that they are bounded at 255 to avoid overflow when querying the p array.
        # Note that this will cause the patterns to repeat every 256 coordinates.
        xi = int(x) & 255
        yi = int(y) & 255
        zi = int(z) & 255

        # Calculate the point's location (from 0.0 to 1.0) inside its unit cube.
        xf = x - int(x)
        yf = y - int(y)
        zf = z - int(z)

        # Apply the fade function - enables smoother seams between unit cubes after
        # vectors are dotted
        u = self.fade(xf)
        v = self.fade(yf)
        w = self.fade(zf)

        # Hash function for all 8 unit cube coordinates surrounding the input coordinate
        # Note that this could be replaced with a random number generator with a constant
        # seed but that could bottleneck performance -> https://stackoverflow.com/q/45625145
        aaa = self.p[self.p[self.p[         xi ] +          yi ] +          zi ]
        aba = self.p[self.p[self.p[         xi ] + self.inc(yi)] +          zi ]
        aab = self.p[self.p[self.p[         xi ] +          yi ] + self.inc(zi)]
        abb = self.p[self.p[self.p[         xi ] + self.inc(yi)] + self.inc(zi)]
        baa = self.p[self.p[self.p[self.inc(xi)] +          yi ] +          zi ]
        bba = self.p[self.p[self.p[self.inc(xi)] + self.inc(yi)] +          zi ]
        bab = self.p[self.p[self.p[self.inc(xi)] +          yi ] + self.inc(zi)]
        bbb = self.p[self.p[self.p[self.inc(xi)] + self.inc(yi)] + self.inc(zi)]

        # Putting it all together - the gradient function calculates the dot product between the
        # pseudorandom gradient vector and the vector from the input coordinate to the 8 urrounding
        # points in its unit cube. This is all combined via linear interpolation as a sort of weighted
        # average of faded values (u,v,w)
        x1 = self.lerp(self.gradient(aaa, xf  , yf  , zf), self.gradient(baa, xf-1, yf  , zf), u)
        x2 = self.lerp(self.gradient(aba, xf  , yf-1, zf), self.gradient(bba, xf-1, yf-1, zf), u)
        y1 = self.lerp(x1, x2, v)

        x1 = self.lerp(self.gradient(aab, xf  , yf  , zf-1), self.gradient(bab, xf-1, yf  , zf-1), u)
        x2 = self.lerp(self.gradient(abb, xf  , yf-1, zf-1), self.gradient(bbb, xf-1, yf-1, zf-1), u)
        y2 = self.lerp(x1, x2, v)

        return (self.lerp(y1, y2, w) + 1) / 2


    def inc(self, num: int) -> int:
        # Increment with allowence for repetition
        num += 1
        if self.repeat > 0: num %= self.repeat
        return num


    def fade(self, t:float) -> float:  # 6t^5 - 15t^4 + 10t^3
        """
        This function is used to account for artifacts left by the dot product of each
        vector. It causes vectors to have a smoother curve

        t is the value of a vector in an individual dimension (ie. x, y, z, etc.)
        This function must be run once per dimension of the shape we are generating with
        perlin noise (for 2D clouds, twice) to generate the value for a single coordinate.
        """
        # return (6 * m.pow(t , 5)) - (15 * m.pow(t, 4)) + (10 * m.pow(t, 3))
        return t * t * t * (t * (t * 6 - 15) + 10)


    def populate_gradient_dict(self=None) -> defaultdict:
        grad_dict = defaultdict()
        grad_dict[0x0] = lambda x, y, z:  x + y
        grad_dict[0x1] = lambda x, y, z: -x + y
        grad_dict[0x2] = lambda x, y, z:  x - y
        grad_dict[0x3] = lambda x, y, z: -x - y
        grad_dict[0x4] = lambda x, y, z:  x + z
        grad_dict[0x5] = lambda x, y, z: -x + z
        grad_dict[0x6] = lambda x, y, z:  x - z
        grad_dict[0x7] = lambda x, y, z: -x - z
        grad_dict[0x8] = lambda x, y, z:  y + z
        grad_dict[0x9] = lambda x, y, z: -y + z
        grad_dict[0xA] = lambda x, y, z:  y - z
        grad_dict[0xB] = lambda x, y, z: -y - z
        grad_dict[0xC] = lambda x, y, z:  y + x
        grad_dict[0xD] = lambda x, y, z: -y + z
        grad_dict[0xE] = lambda x, y, z:  y - x
        grad_dict[0xF] = lambda x, y, z: -y - z
        return grad_dict
    gradient_dict = populate_gradient_dict()

    

    def gradient(self, hash: int, x: float, y: float, z: float) -> float:
        """
        Serves to randomly choose a vector from the following 12 as detailed in the
        initial paper on Perlin Noise:
        (1,1,0),  (-1,1,0),  (1,-1,0), (-1,-1,0), (1,0,1),  (-1,0,1),
        (1,0,-1), (-1,0,-1), (0,1,1),  (0,-1,1),  (0,1,-1), (0,-1,-1)

        This vector determined by the last 4 bits of the hash function value (the first
        parameter in this function).

        The following 3 parameters represent the location vector to be used for the dot product.
        """
        dict_key = hash & 0xF
        val = dict_key
        return self.gradient_dict[dict_key](x, y,  z)
    

    def lerp(self, a: float, b:float, x:float) -> float:
        # Linear Interpolation!
        return a + x * (b - a)


    # @timing
    def octive_perlin(self, x:float, y:float, z:float, num_octaves: int, persistence:float) -> float:
        """
        Frequency = 2 raised to the number of octaves
        Amplitude = persistance raised to the number of octaves
        Persistance is a measure of how much influence each successive octave has
        """
        total = 0
        frequency = 1
        amplitude = 1
        max_value = 0  # Used for normalizing result to 0.0 to 1.0

        for octave in range(num_octaves):
            new_perlin_val = self.perlin(x * frequency, y * frequency, z * frequency)
            total += (new_perlin_val * amplitude)
            max_value += amplitude
            amplitude *= persistence
            frequency = frequency * 2

        return total / max_value
