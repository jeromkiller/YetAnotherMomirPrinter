from . import GenNoise
import os

from PIL import ImageFile
import matplotlib.image as img
import numpy as np
import math

def DitherImage(imageRaw: ImageFile.ImageFile, ditherTexturePath="noise.png"):
    if not os.path.exists(ditherTexturePath):
        GenNoise.generateNoise(100, 100, path=ditherTexturePath)
    noise = img.imread(ditherTexturePath)
    image = np.array(imageRaw)

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

def toPrintString(image: np.ndarray):
    test = np.array([[1, 4, 7, 10],
                     [2, 5, 8, 11],
                     [3, 6, 9, 12],
                     [13, 15, 17, 19],
                     [14, 16, 18, 20]])
    test = test % 3 == 0
    flattened = np.array([])
    for i in range(math.ceil(test.shape[0] / 3)):
        sliceStart = i * 3
        sliceStop = sliceStart + 3
        flatRow = test[:][sliceStart:sliceStop].flatten('F')
        flattened = np.append(flattened, flatRow)
    flattened = flattened.astype(int)
    print(flattened)
    packed = np.packbits(flattened)
    print(packed)


if __name__ == "__main__":
    toPrintString(np.array([]))
    exit()

    image_path = "example.jpg"
    image = img.imread(image_path)

    dithered = DitherImage(image)

    img.imsave("dithered.png", dithered, cmap="gray")    
    