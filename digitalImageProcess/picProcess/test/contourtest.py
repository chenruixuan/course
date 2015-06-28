from PIL import Image
from pylab import *

im = array(Image.open('seu.jpg').convert('L'))

figure()
gray()

imshow(im)

figure()
contour(im, origin='image')
#axis('equal')
#axis('off')

#figure()
#hist(im.flatten(),128)
show()