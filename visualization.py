import pandas as pd
import numpy as np
import perlin as per
from matplotlib import cm
from PIL import Image

def perlin_dataframe(df_len:int, df_height:int) -> pd.DataFrame:
    perlin_obj = per.Perlin()
    perlin_df = pd.DataFrame(index=range(df_len),
                             columns=range(df_height))
    
    # Apply perlin function to every cell in perlin_df
    # perlin_df = perlin_df.applymap(lambda x: perlin_obj.perlin(x, x % , 0))
    for x in range(0, df_len):
        for y in  range(0, df_height):
            perlin_df.iat[x,y] = perlin_obj.perlin(x / 255, y / 255, 0.5)
            
    return perlin_df


def two_d_vis(img_len:int=1000, img_height:int=1000):
    perlin_df = perlin_dataframe(img_len, img_height)
    print(perlin_df)
    # Create base image    
    img = Image.fromarray(np.uint8(perlin_df.to_numpy()*255))
    img.show()
two_d_vis()

    