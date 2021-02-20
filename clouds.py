from PIL import Image

print("Hey")
im = Image.new("RGB", (500, 700), (255, 0, 0))
im.show()
print("Done")

class Perlin:
    def __init__(self):
        pass

    repeat = -1

    permutation = [151,160, 137,91,90,15,131, 13,201,95,96,53, 194,233,7,225,140,36,
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

    p = []

    def perlin(self, x, y, z):
        if (self.repeat > 0):
            x = x % self.repeat
            y = y % self.repeat
            z = z % self.repeat

        xi = int(x) & 255
        yi = int(y) & 255
        zi = int(z) & 255

        xf = x - int(x)
        yf = y - int(y)
        zf = z - int(z)

        u = self.fade(xf)
        v = self.fade(yf)
        w = self.fade(zf)

        aaa = self.p[self.p[self.p[         xi ] +          yi ] +          zi ]
        aba = self.p[self.p[self.p[         xi ] + self.inc(yi)] +          zi ]
        aab = self.p[self.p[self.p[         xi ] +          yi ] + self.inc(zi)]
        abb = self.p[self.p[self.p[         xi ] + self.inc(yi)] + self.inc(zi)]
        baa = self.p[self.p[self.p[self.inc(xi)] +          yi ] +          zi ]
        bba = self.p[self.p[self.p[self.inc(xi)] + self.inc(yi)] +          zi ]
        bab = self.p[self.p[self.p[self.inc(xi)] +          yi ] + self.inc(zi)]
        bbb = self.p[self.p[self.p[self.inc(xi)] + self.inc(yi)] + self.inc(zi)]

        x1 = self.lerp(self.grad(aaa, xf  , yf  , zf), self.grad(baa, xf-1, yf  , zf), u)
        x2 = self.lerp(self.grad(aba, xf  , yf-1, zf), self.grad(bba, xf-1, yf-1, zf), u)
        y1 = self.lerp(x1, x2, v)

        x1 = self.lerp(self.grad(aab, xf  , yf  , zf-1), self.grad(bab, xf-1, yf  , zf-1), u)
        x2 = self.lerp(self.grad(abb, xf  , yf-1, zf-1), self.grad(bbb, xf-1, yf-1, zf-1), u)
        y2 = self.lerp(x1, x2, v)

        return (self.lerp(y1, y2, w) + 1) / 2


    def inc(self, num):
        num += 1
        if repeat > 0: num %= repeat
        return num	


    def fade(self, t):
        return t * t * t * (t * (t * 6 - 15) + 10);       # 6t^5 - 15t^4 + 10t^3

    def grad(self, hash, x, y, z):
        val = hash & 0xF
        if   val == 0x0: return  x + y
        elif val == 0x1: return -x + y
        elif val == 0x2: return  x - y
        elif val == 0x3: return -x - y
        elif val == 0x4: return  x + z
        elif val == 0x5: return -x + z
        elif val == 0x6: return  x - z
        elif val == 0x7: return -x - z
        elif val == 0x8: return  y + z
        elif val == 0x9: return -y + z
        elif val == 0xA: return  y - z
        elif val == 0xB: return -y - z
        elif val == 0xC: return  y + x
        elif val == 0xD: return -y + z
        elif val == 0xE: return  y - x
        elif val == 0xF: return -y - z
        else: return 0

    def lerp(self, a, b, x):
        return a + x * (b - a)

    def octive_perlin(self, x:float, y:float, z:float, num_octaves: int, persistence:float) -> float:
        total = 0
        frequency = 1
        amplitude = 1
        max_value = 0  # Used for normalizing result to 0.0 to 1.0

        for octave in range(num_octaves):
            new_perlin_val = perlin(x * frequency, y * frequency, z * frequency)
            total += (new_perlin_val * amplitude)
            max_value += amplitude
            amplitude *= persistence
            frequency = frequency * 2

        return total / max_value
