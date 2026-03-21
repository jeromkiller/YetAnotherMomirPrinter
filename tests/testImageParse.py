import unittest
from PIL import Image
from src.MomirVig import ProcessImage
import numpy as np

class TestCardParsing(unittest.TestCase):
    def test_slice(self):
        data = np.arange(16).reshape(4, 4)
        slices = ProcessImage.sliceImage(data, 2)
        self.assertEqual(len(slices), 2)
        self.assertTupleEqual(slices[0].shape, (2, 4))
        self.assertListEqual(slices[0].tolist(), [[0, 1, 2, 3], [4, 5 ,6 ,7]])
        self.assertListEqual(slices[1].tolist(), [[8, 9, 10, 11], [12, 13, 14, 15]])

    def test_small_slices(self):
        data = np.arange(16).reshape(4, 4)
        slices = ProcessImage.sliceImage(data, 3)
        self.assertEqual(len(slices), 2)
        self.assertTupleEqual(slices[0].shape, (3, 4))
        self.assertTupleEqual(slices[1].shape, (3, 4))
        self.assertListEqual(slices[0].tolist(), [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]])
        self.assertListEqual(slices[1].tolist(), [[12, 13, 14, 15], [0, 0, 0, 0], [0, 0, 0, 0]])

    def test_transpose(self):
        data = np.array([[0, 3, 6, 9, 12, 15],
                         [1, 4, 7, 10, 13, 16],
                         [2, 5, 8, 11, 14, 17]])
        correct = [[0, 1, 2, 3, 4, 5],
                   [6, 7, 8, 9, 10, 11],
                   [12, 13, 14, 15, 16, 17]]
        transposed = ProcessImage.transposeSlice(data)
        self.assertTupleEqual(transposed.shape, data.shape, "output should be same shape as input")
        self.assertListEqual(transposed.tolist(), correct)


    def test_small_transposition(self):
        image = Image.open("tests/resources/up_small.png")
        image_check = Image.open("tests/resources/up_small_transposed.png")
        image = ProcessImage.DitherImage(image)
        image_check = ProcessImage.DitherImage(image_check)
        image_transposed = ProcessImage.toPrintStrings(image, 24)[0]
        image_check = np.packbits(image_check)
        self.assertEqual(image_transposed, image_check)