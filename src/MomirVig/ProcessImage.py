from . import GenNoise
import os

from PIL import ImageFile, Image
import matplotlib.image as img
import numpy as np
import math

def DitherImage(imageRaw: ImageFile.ImageFile | Image.Image, max_width: int | None = None, max_height: int | None = None, ditherTexturePath="noise.png", negative: bool = False) -> np.ndarray:
    imageResize = resizeImage(imageRaw, max_width, max_height)

    if not os.path.exists(ditherTexturePath):
        GenNoise.generateNoise(100, 100, path=ditherTexturePath)
    noise = img.imread(ditherTexturePath)
    image = np.array(imageResize)

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

    if negative:
        dithered = dithered != True
    
    return dithered

def resizeImage(image: ImageFile.ImageFile | Image.Image, max_width: int | None = None, max_height: int | None = None) -> Image.Image:
    # resize the image horizontally
    imageResize = image
    if max_width:
        if imageResize.width > max_width:
            resize_factor = max_width / imageResize.width
            imageResize = imageResize.resize((max_width, int(imageResize.height * resize_factor)))

    # resize the image vertically
    if max_height:
        if imageResize.height > max_height:
            resize_factor = max_height / imageResize.height
            imageResize = imageResize.resize((int(imageResize.width * resize_factor), max_height))
    return imageResize


def sliceImage(image: np.ndarray, tile_size: int) -> list[np.ndarray]:
    slices = list[np.ndarray]()
    for slice_index in range(math.ceil(image.shape[0] / tile_size)):
        sliceStart = slice_index * tile_size
        sliceEnd = sliceStart + tile_size
        image_slice = image[:][sliceStart:sliceEnd]
        if image_slice.shape[0] != tile_size:
            width = image_slice.shape[1]
            height = tile_size - image_slice.shape[0]
            new_row = np.zeros((height, width), dtype=image_slice.dtype)
            image_slice = np.concatenate((image_slice, new_row), axis=0)

        slices.append(image_slice)
    return slices

def transposeSlice(slice: np.ndarray) -> np.ndarray:
    shape = slice.shape
    transposed = slice.transpose()
    reshaped = transposed.reshape(shape)
    return reshaped


def toPrintStrings(image: np.ndarray, tile_size: int) -> list[bytearray]:
    byte_arrays = list[bytearray]()
    for slice in sliceImage(image, tile_size):
        transposed = transposeSlice(slice)
        flatrow = transposed.flatten('C')
        byte_data = bytearray(np.packbits(flatrow))
        byte_arrays.append(byte_data)
    return byte_arrays
