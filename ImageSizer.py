__author__ = 'dbaker'

from PIL import Image
import pexif


def getRatio(image, resizeTo):
    longEdge = max(image.size[0], image.size[1])
    return float(longEdge) / resizeTo


def getNewSize(originalSize, ratio):
    newWidth = originalSize[0] / ratio
    newHeight = originalSize[1] / ratio
    return int(newWidth), int(newHeight)


ext = ".jpg"

# Command Line Arg
imageName = 'fullsized_image'

originalImage = Image.open(imageName + ext)

#Command Line arg
setLongestEdgeTo = 500

newSize = getNewSize(originalImage.size, getRatio(originalImage, setLongestEdgeTo))

newImage = originalImage.resize((newSize[0], newSize[1]), Image.ANTIALIAS)  # best down-sizing filter

newImageName = imageName + "_" + str(setLongestEdgeTo) + ext
newImage.save(newImageName)

img_src = pexif.JpegFile.fromFile(imageName + ext)
img_dst = pexif.JpegFile.fromFile(newImageName)
img_dst.import_exif(img_src.exif)
img_dst.writeFile("hello4.jpg")
