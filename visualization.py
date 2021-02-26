import pandas as pd
import numpy as np
import perlin_optimized as per
from timing import timing
from PIL import Image, ImageDraw
from pyinstrument import Profiler

@timing
def perlin_matrix(len:int, height:int, num_octives:int, persistence:float) -> pd.DataFrame:
    perlin_obj = per.Perlin()
    perlin_matrix = [[0 for x in range(len)] for y in range(height)]

    # Apply perlin function to every cell in perlin_df
    for x in range(0, len):
        for y in  range(0, height):
            perlin_matrix[x][y] = \
                perlin_obj.octive_perlin(x / 255, y / 255, 0.5,
                                         num_octives, persistence)

    return perlin_matrix


def two_d_vis(img_len:int=500, img_height:int=500, num_octaves:int=1, persistence:int=1):
    profiler.start()
    perlin_df = perlin_matrix(img_height, img_len, num_octaves, persistence)
    profiler.stop()

    # Labeling
    label_str = "Octaves: " + str(num_octaves) + "\nPersistence: " + str(persistence)
    file_name_str = "perlin_2d_vis_" + str(num_octaves) + "_octaves_" + str(persistence) + \
        "_persistence.jpeg"

    # Render and save image
    img = Image.fromarray(np.uint8(np.array(perlin_df)*255))
    img_with_label = ImageDraw.Draw(img)
    img_with_label.text((50,50), label_str)
    img.save("perlin_images/" + file_name_str)

profiler = Profiler()
two_d_vis(num_octaves=1, persistence=.5)
print(profiler.output_text(unicode=True, color=True))
