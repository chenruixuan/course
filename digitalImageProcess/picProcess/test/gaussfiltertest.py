#encoding: utf-8
from PIL import Image
from numpy import *
from pylab import *
from scipy.ndimage import filters

im = array(Image.open('tiger.jpg').convert('L'))
gray()

sigma = 2
imx = zeros(im.shape)
filters.gaussian_filter(im, (sigma, sigma), (0, 1), imx)

imy = zeros(im.shape)
filters.gaussian_filter(im, (sigma, sigma), (1, 0), imy)

magnitude = sqrt(imx**2 + imy**2)

imshow(im)
figure()
imshow(magnitude)

show()