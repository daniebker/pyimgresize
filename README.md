# PyImgResize #

# Description #

PyImgResize is a python script that resizes an image file, or a folder or image files, to a specific size. It preserves the original ratio of the image by resizing the longest edge of the image.

# Usage #

## Help ##

`python pyimgresize.py -h`

## Resize a folder of images longest edge to 500px ##

`python pyimgresize.py -le 500 -f "C:\Some\Path\To\Images\"`

## Set the ouput format to jpg ##

`python pyimgresize.py -le 500 -f "C:\Some\Path\To\Images\" -of ".jpg"`

## Notes ##

Images will be saved on the same path with the following format:

`[ORIGINAL_NAME]_[WIDTH]x[HEIGH].[FORMAT]`

