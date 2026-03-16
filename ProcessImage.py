import GenNoise
import os

import matplotlib.image as img
import numpy as np
import math

def DitherImage(imageRaw, ditherTexturePath="noise.png"):
    if not os.path.exists(ditherTexturePath):
        GenNoise.generateNoise(100, 100, path=ditherTexturePath)
    noise = img.imread(ditherTexturePath)
    image = imageRaw.copy()

    if np.max(image) > 1:
        # assume this is not a png
        image = image / 255

    image = np.dot(image[...,:3], [0.2989, 0.5870, 0.1140]) # to gray scale
    noise = np.dot(noise[...,:1], [1])  # there's probably a better way to do this

    h_tile = math.ceil(image.shape[0] / noise.shape[0])
    v_tile = math.ceil(image.shape[1] / noise.shape[1])

    noise = np.tile(noise, (h_tile, v_tile))
    noise = noise[:image.shape[0], :image.shape[1]]
    dithered = image >= noise
    
    return dithered

if __name__ == "__main__":
    image_path = "example.jpg"
    image = img.imread(image_path)

    dithered = DitherImage(image)

    img.imsave("dithered.png", dithered, cmap="gray")    
    