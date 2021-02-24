import pandas as pd
import numpy as np
import PIL as pil
import perlin as per

def two_d_vis(img_len:int=500, img_height:int=500):
    perlin_obj = per.Perlin()

    perlin_df = pd.DataFrame(index=range(img_height),
                             columns=range(img_len))
    
    # Apply perlin function to every cell in perlin_df
    # perlin_df = perlin_df.applymap(lambda x: perlin_obj.perlin(x, x % , 0))
    
    for x in range(0, 500):
        for y in  range(0, 500):
            perlin_df.iat[x,y] = perlin_obj.perlin(x, y, 0)
            
    pass

two_d_vis()

    