#!/usr/bin/env python
# encoding: utf-8
"""
pyimgresize.py
Created on 26/04/2016
Copyright (c) D. Baker. All rights reserved.

"""

import os


class ImageFile:
    def __init__(self, file_path, width, height):
        self.file_path = file_path
        self.width = width
        self.height = height

    @property
    def image_name(self):
        return os.path.splitext(os.path.basename(self.file_path))[0]

    @property
    def image_ext(self):
        return os.path.splitext(os.path.basename(self.file_path))[1]

    @property
    def image_directory(self):
        return os.path.dirname(self.file_path)


def get_ratio(target_size, width, height):
    long_edge = max(width, height)
    if target_size < long_edge:
        return float(long_edge) / target_size
    else:
        return long_edge


def get_new_size(ratio, width, height):
    new_width = width / ratio
    new_height = height / ratio
    return int(new_width), int(new_height)


def resize_longest_edge_to(longest_edge, original_image):
    ratio = get_ratio(longest_edge, original_image.width, original_image.height)
    new_size = get_new_size(ratio, original_image.width, original_image.height)
    new_image_name = original_image.image_name + "_" + str(longest_edge) + original_image.image_ext
    new_image_file_path = original_image.image_directory + os.path.sep + new_image_name
    return ImageFile(new_image_file_path, new_size[0], new_size[1])
