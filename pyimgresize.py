#!/usr/bin/env python
# encoding: utf-8
"""
pyimgresize.py
Created on 26/04/2016
Copyright (c) D. Baker.
"""

import os
import piexif

from PIL import Image

__author__ = 'daniebker'


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
        for filename in file_names:
            if filter_image_file(filename):
                matches.append(os.path.join(root, filename))
    return matches


def filter_image_file(filename):
    file_types = ['.jpg', '.tif', '.jpeg']
    for file_type in file_types:
        if filename.endswith(file_type):
            return True

    return False


def resize_images(longest_edge, images):
    resized_images = []
    for image in images:
        resized_images.append(resize_longest_edge_to(longest_edge, image))

    return resized_images


def get_pil_format(output_format):
    return {
        '.jpg': 'JPEG',
        '.jpeg': 'JPEG',
        '.tif': 'TIFF'
    }[output_format]  # will throw when key not found.


def save_image_to_disk(resized_image, output_format=None):
    pil_original_image = Image.open(resized_image.file_path)

    exif_bytes = extract_exif_bytes(pil_original_image)

    if output_format is None:
        output_format = resized_image.image_ext

    try:
        pil_format = get_pil_format(output_format)
    except KeyError:
        return "FAIL", "Unhandled output format {output_format}".format(output_format=output_format)

    pil_resized_image = pil_original_image.resize(
        (resized_image.width, resized_image.height),
        Image.ANTIALIAS)

    new_image_name = resized_image.image_name \
                     + "_" + str(resized_image.width) + "x" + str(resized_image.height) \
                     + output_format

    new_image_file_path = resized_image.image_directory + os.path.sep + new_image_name

    try:
        if exif_bytes is not None:
            pil_resized_image.save(new_image_file_path, format=pil_format, exif=exif_bytes)
            result = ("OK", "Saved {file_name} with exif data".format(file_name=new_image_name))
        else:
            pil_resized_image.save(new_image_file_path, format=pil_format)
            result = ("WARN", "Saved {file_name} without exif data".format(file_name=new_image_name))
    except KeyError:
        result = ("FAIL", "Failed to save image as {file_type}".format(file_type=output_format))

    return result


def extract_exif_bytes(pil_original_image):
    try:
        exif_dict = piexif.load(pil_original_image.info["exif"])
        return piexif.dump(exif_dict)
    except KeyError:
        return None


def validate_output_format(output_format):
    if not output_format.startswith('.'):
        return False, "Format must start with a period"

    return True, "output format is valid"


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", help="The file path to your image or images.")
    parser.add_argument("-le", help="The size to set the longest edge to.", type=int)
    parser.add_argument("-of", help="The file output format to save as. Defaults to original file format")
    args = parser.parse_args()

    if args.of is not None:
        valid, message = validate_output_format(args.of)

        if not valid:
            if message == "Format must start with a period":
                print(message)
                print("Adding a period to the beginning of the format")
                args.of = "." + args.of

    for path in get_files_on_path(args.f):
        result, message = save_image_to_disk(
            resize_longest_edge_to(args.le, open_image_file(path)), args.of)

        print(message)


if __name__ == '__main__':
    main()
