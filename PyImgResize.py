#!/usr/bin/env python
# encoding: utf-8
"""
pyimgresize.py
Created on 26/04/2016
Copyright (c) D. Baker. All rights reserved.

"""

import os
import fnmatch, argparse

from PIL import Image


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


def open_image_file(path):
    pil_image = Image.open(path)
    return ImageFile(path, pil_image.size[0], pil_image.size[1])


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
    return ImageFile(original_image.file_path, new_size[0], new_size[1])


def get_files_on_path(path):
    matches = []
    for root, dir_names, file_names in os.walk(path):
        for filename in fnmatch.filter(file_names, '*.jpg'):
            matches.append(os.path.join(root, filename))
    return matches


def resize_images(longest_edge, images):
    resized_images = []
    for image in images:
        resized_images.append(resize_longest_edge_to(longest_edge, image))

    return resized_images


def save_image_to_disk(resized_image):
    pil_original_image = Image.open(resized_image.file_path)
    pil_resized_image = pil_original_image.resize((resized_image.width, resized_image.height), Image.ANTIALIAS)

    new_image_name = resized_image.image_name \
                     + "_" + str(resized_image.width) + "x" + str(resized_image.height) \
                     + resized_image.image_ext
    new_image_file_path = resized_image.image_directory + os.path.sep + new_image_name

    pil_resized_image.save(new_image_file_path)


parser = argparse.ArgumentParser()
parser.add_argument("-f", help="The file path to your image or images.")
parser.add_argument("-le", help="The size to set the longest edge to.", type=int)
args = parser.parse_args()

resized_image_files = []
for path in get_files_on_path(args.f):
    resized_image_files.append(resize_longest_edge_to(args.le, open_image_file(path)))

for resized_image in resized_image_files:
    save_image_to_disk(resized_image)
