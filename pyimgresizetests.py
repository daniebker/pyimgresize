#!/usr/bin/env python
# encoding: utf-8

from unittest.mock import patch
import unittest

import pyimgresize
from pyimgresize import ImageFile

__author__ = 'daniebker'


class ImgResizeTests(unittest.TestCase):
    def test_get_ratio(self):
        result = pyimgresize.get_ratio(200, 600, 200)
        self.assertEqual(3, result)

    def test_get_new_size(self):
        result = pyimgresize.get_new_size(3, 600, 300)
        self.assertEqual(200, result[0])
        self.assertEqual(100, result[1])

    def test_resize_longest_edge_to(self):
        expected = ImageFile("C:\\some\\path\\to\\file.jpg", 200, 100)
        result = pyimgresize.resize_longest_edge_to(200, ImageFile("C:\\some\\path\\to\\file.jpg", 600, 300))
        self.assert_images_are_equal(expected, result)

    def test_resize_images(self):
        expected = []
        for count in range(4):
            image_file = ImageFile("C:\\some\\path\\to\\file_" + str(count) + ".jpg", 200, 100)
            expected.append(image_file)

        images_to_resize = []
        for count in range(4):
            image_file = ImageFile("C:\\some\\path\\to\\file_" + str(count) + ".jpg", 600, 300)
            images_to_resize.append(image_file)

        result = pyimgresize.resize_images(200, images_to_resize)

        for ii in range(len(expected) - 1):
            self.assert_images_are_equal(expected[ii], result[ii])

    @patch('pyimgresize.os.walk')
    def test_get_files_on_path(self, mock):
        mock.return_value = [
            ('C:\\some\\path\\to\\file', (), ('foo.txt',))
        ]

        matches = pyimgresize.get_files_on_path("C:\\some\\path\\to\\file")
        self.assertEqual(0, len(matches))

    @patch('pyimgresize.os.walk')
    def test_get_files_on_path_with_jpgs(self, mock):
        mock.return_value = [
            ('C:\\some\\path\\to\\file', (), ('foo.jpg',))
        ]
        matches = pyimgresize.get_files_on_path("C:\\some\\path\\to\\file")
        self.assertEqual(1, len(matches))

    @patch('pyimgresize.os.walk')
    def test_get_files_on_path_with_tif(self, mock):
        mock.return_value = [
            ('C:\\some\\path\\to\\file', (), ('foo.tif',))
        ]
        matches = pyimgresize.get_files_on_path("C:\\some\\path\\to\\file")
        self.assertEqual(1, len(matches))

    @patch('pyimgresize.os.walk')
    def test_get_files_on_path_with_multiple_file_types(self, mock):
        expected = [
            ('C:\\some\\path\\to\\file', (), ('foo.tif',)),
            ('C:\\some\\path\\to\\file', (), ('foo.jpg',)),
            ('C:\\some\\path\\to\\file', (), ('foo.jpeg',))
        ]
        mock.return_value = expected
        matches = pyimgresize.get_files_on_path("C:\\some\\path\\to\\file")
        self.assertEqual(len(expected), len(matches))

    def test_validate_save_as_not_start_with_period(self):
        result = pyimgresize.validate_output_format("jpeg")

        self.assertFalse(result)

    def assert_images_are_equal(self, expected, result):
        self.assertEqual(expected.file_path, result.file_path)
        self.assertEqual(expected.width, result.width)
        self.assertEqual(expected.height, result.height)


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
