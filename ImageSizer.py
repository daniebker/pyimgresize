__author__ = 'dbaker'

from PIL import Image

ext = ".jpg"

#Command Line Arg
imageName = 'fullsized_image'

originalImage = Image.open(imageName + ext)

#Command Line arg
resizeTo = 500

longEdge = max(originalImage.size[0], originalImage.size[1])
ratio = float(longEdge)/resizeTo

newWidth = originalImage.size[0] / ratio
newHeight = originalImage.size[1] / ratio

newImage = originalImage.resize((int(newWidth), int(newHeight)), Image.ANTIALIAS)    # best down-sizing filter

newImage.save(imageName + "_" + str(resizeTo) + ext)