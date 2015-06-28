from PIL import Image
from pylab import *
import matplotlib.cm

im = array(Image.open('tiger.jpg').convert('L'))
imshow(im, cmap=matplotlib.cm.Greys_r)
show()