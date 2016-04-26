#!/usr/bin/env python
# encoding: utf-8
"""
pyimgresize.py
Created on 26/04/2016
Copyright (c) D. Baker. All rights reserved.

"""

import argparse
import os
import fnmatch


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