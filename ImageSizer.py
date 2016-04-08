__author__ = 'dbaker'

from ResizeableImage import ResizableImage
import argparse
import os
import fnmatch


parser = argparse.ArgumentParser()
parser.add_argument("-f", help="The file path to your image or images.")
parser.add_argument("-le", help="The size to set the longest edge to.", type=int)
args = parser.parse_args()

setLongestEdgeTo = args.le

if os.path.isdir(args.f):
    matches = []
    for root, dir_names, file_names in os.walk(args.f):
        for filename in fnmatch.filter(file_names, '*.jpg'):
            matches.append(os.path.join(root, filename))

    for original_image_file_path in matches:
        resizeable_image = ResizableImage(original_image_file_path)
        print 'Setting longest edge to ' + str(args.le) + ' for ' + original_image_file_path
        resizeable_image.resize_longest_edge_to(args.le)  # best down-sizing filter
else:
    resizeable_image = ResizableImage(args.f)
    resizeable_image.resize_longest_edge_to(args.le)  # best down-sizing filter
