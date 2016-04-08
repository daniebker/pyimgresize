__author__ = 'dbaker'

from PIL import Image
import os
import pexif


class ResizableImage:
    """A resizeable image object

    Attributes:
        original_image_file_path: the full file path to the image.
        dir_name: the directory name the image resides in.
        image_name: the file name of the image.
        ext: the extension of the image.
        original_image: a PIL Image object of the original image.
    """

    def __init__(self, original_image_file_path):
        self.original_image_file_path = original_image_file_path
        self.dir_name = os.path.dirname(self.original_image_file_path)
        self.image_name, self.ext = os.path.splitext(os.path.basename(self.original_image_file_path))
        self.original_image = Image.open(self.original_image_file_path)

    """
        Gets the ratio of the new image based on the target size.
        If the target size is greater than the longest edge of the
        image then it just returns the longest edge.
    """
    def get_ratio(self, target_size):
        long_edge = max(self.original_image.size[0], self.original_image.size[1])
        if target_size < long_edge:
            return float(long_edge) / target_size
        else:
            return long_edge

    def get_new_size(self, ratio):
        new_width = self.original_image.size[0] / ratio
        new_height = self.original_image.size[1] / ratio
        return int(new_width), int(new_height)

    """
    This doesn't feel like it belongs here.
    """
    def set_exif_data(self, new_image_file_path):
        img_src = pexif.JpegFile.fromFile(self.original_image_file_path)
        img_dst = pexif.JpegFile.fromFile(new_image_file_path)
        img_dst.import_exif(img_src.exif)
        img_dst.writeFile(new_image_file_path)

    """
    This also feels like it doesn't belong here.
    """
    def resize_longest_edge_to(self, size):
        new_size = self.get_new_size(self.get_ratio(size))
        resized_image = self.original_image.resize((new_size[0], new_size[1]), Image.ANTIALIAS)
        new_image_name = self.image_name + "_" + str(size) + self.ext
        new_image_file_path = self.dir_name + os.path.sep + str(size) + os.path.sep + new_image_name

        if not os.path.exists(os.path.dirname(new_image_file_path)):
            os.makedirs(os.path.dirname(new_image_file_path))

        resized_image.save(new_image_file_path)
        self.set_exif_data(new_image_file_path)
