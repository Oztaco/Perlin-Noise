import pandas as pd
import numpy as np
import perlin as per
from timing import timing
from PIL import Image, ImageDraw

@timing
def perlin_dataframe(df_len:int, df_height:int, num_octives:int, persistence:float) -> pd.DataFrame:
    perlin_obj = per.Perlin()
    perlin_df = pd.DataFrame(index=range(df_len),
                             columns=range(df_height))

    # Apply perlin function to every cell in perlin_df
    # perlin_df = perlin_df.applymap(lambda x: perlin_obj.perlin(x, x % , 0))
    for x in range(0, df_len):
        for y in  range(0, df_height):
            perlin_df.iat[x,y] = perlin_obj.octive_perlin(x / 255,
                                                          y / 255,
                                                          0.5,
                                                          num_octives,
                                                          persistence)

    return perlin_df


def two_d_vis(img_len:int=500, img_height:int=500, num_octaves:int=1, persistence:int=1):
    perlin_df = perlin_dataframe(img_height, img_len, num_octaves, persistence)

    # Labeling
    label_str = "Octaves: " + str(num_octaves) + "\nPersistence: " + str(persistence)
    file_name_str = "perlin_2d_vis_" + str(num_octaves) + "_octaves_" + str(persistence) + \
        "_persistence.jpeg"

    # Render and save image
    img = Image.fromarray(np.uint8(perlin_df.to_numpy()*255))
    img_with_label = ImageDraw.Draw(img)
    img_with_label.text((50,50), label_str)
    img.save("perlin_images/" + file_name_str)

two_d_vis(num_octaves=1, persistence=.5)