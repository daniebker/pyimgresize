__author__ = 'dbaker'

import unittest
import pyimgresize
from pyimgresize import ImageFile


class ImgResizeTests(unittest.TestCase):
    def test_get_ratio(self):
        result = pyimgresize.get_ratio(200, 600, 200)
        self.assertEqual(3, result)

    def test_get_new_size(self):
        result = pyimgresize.get_new_size(3, 600, 300)
        self.assertEqual(200, result[0])
        self.assertEqual(100, result[1])

    def test_resize_longest_edge_to(self):
        expected = ImageFile("C:\\some\\path\\to\\file_200.jpg", 200, 100)
        result = pyimgresize.resize_longest_edge_to(200, ImageFile("C:\\some\\path\\to\\file.jpg", 600, 300))
        self.assertEquals(expected.file_path, result.file_path)
        self.assertEquals(expected.width, result.width)
        self.assertEquals(expected.height, result.height)

class ImageFileTestCase(unittest.TestCase):
    def setUp(self):
        self.image_file = ImageFile("C:/some/path/to/file.jpg", 800, 600)

    def tearDown(self):
        self.image_file = None

    def test_image_name(self):
        self.assertEqual("file", self.image_file.image_name)

    def test_image_ext(self):
        self.assertEqual(".jpg", self.image_file.image_ext)

    def test_image_directory(self):
        self.assertEqual("C:/some/path/to", self.image_file.image_directory)


if __name__ == '__main__':
    unittest.main()
