#encoding: utf-8
from PIL import Image
from pylab import *

im = array(Image.open('seu.jpg').convert('L'))
gray()

"""对一幅灰度图进行直方图均衡化"""
# 计算图像的直方图
imhist, bins = histogram(im.flatten(), 256, normed=True)
cdf = imhist.cumsum() # 累积分布函数
cdf = 255 * cdf / cdf[-1] # 归一化
# 使用累积分布函数的线性插值，计算新的像素值
im2 = interp(im.flatten(), bins[:-1], cdf)
im = im2.reshape(im.shape)
imshow(im)

show()
