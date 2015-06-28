#encoding: utf-8
# 把str编码由ascii改为utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import os
import wx
import rof
from PIL import Image
from scipy.ndimage import filters
from wxMatplotlib import MPL_Panel,MPL_Frame,pylab,pyplot,np

class wxMPL_Frame(MPL_Frame):  
    def __init__(self,title="PicProcess_v1.0",size=(850,500)):  
        MPL_Frame.__init__(self,title=title,size=size)  
        self.Button1.SetLabel('(Open)打开')  

        self.btnReset = wx.Button(self.RightPanel,-1,"(Reset)重置",size=(150,40))
        self.btnReset.Bind(wx.EVT_BUTTON,self.btnResetEvent)
        self.FlexGridSizer.Add(self.btnReset,proportion =0, border = 5,flag = wx.ALL | wx.EXPAND)

        self.btnSave = wx.Button(self.RightPanel,-1,"(Save)保存",size=(200,40))
        self.btnSave.Bind(wx.EVT_BUTTON,self.btnSaveEvent)
        self.FlexGridSizer.Add(self.btnSave,proportion =0, border = 5,flag = wx.ALL | wx.EXPAND)

        self.btnReverse = wx.Button(self.RightPanel,-1,"反相",size=(150,40))
        self.btnReverse.Bind(wx.EVT_BUTTON,self.btnReverseEvent)
        self.FlexGridSizer.Add(self.btnReverse,proportion =0, border = 5,flag = wx.ALL | wx.EXPAND)

        self.btnBalance = wx.Button(self.RightPanel,-1,"直方图均衡化",size=(150,40))
        self.btnBalance.Bind(wx.EVT_BUTTON,self.btnBalanceEvent)
        self.FlexGridSizer.Add(self.btnBalance,proportion =0, border = 5,flag = wx.ALL | wx.EXPAND)

        self.btnGaussFilter = wx.Button(self.RightPanel,-1,"高斯导数滤波（图像分割）",size=(200,40))
        self.btnGaussFilter.Bind(wx.EVT_BUTTON,self.btnGaussFilterEvent)
        self.FlexGridSizer.Add(self.btnGaussFilter,proportion =0, border = 5,flag = wx.ALL | wx.EXPAND)

        self.btnDenoise = wx.Button(self.RightPanel,-1,"ROF去噪",size=(200,40))
        self.btnDenoise.Bind(wx.EVT_BUTTON,self.btnDenoiseEvent)
        self.FlexGridSizer.Add(self.btnDenoise,proportion =0, border = 5,flag = wx.ALL | wx.EXPAND)

        self.btnAbout = wx.Button(self.RightPanel,-1,"(About)关于本软件",size=(200,40))
        self.btnAbout.Bind(wx.EVT_BUTTON,self.btnAboutEvent)
        self.FlexGridSizer.Add(self.btnAbout,proportion =0, border = 5,flag = wx.ALL | wx.EXPAND)

    def Button1Event(self,event):
        self.DoOpenFile()

    def btnResetEvent(self, event):
        """重置图片，撤销所有修改"""
        self.im = pylab.array(Image.open(self.picpath).convert('L'))
        self.displayImage()

    def btnReverseEvent(self, event):
        """对一幅灰度图进行反相"""
        assert self.picName != None
        self.im = 255 - self.im
        self.displayImage()

    def btnBalanceEvent(self, event):
        """对一幅灰度图进行直方图均衡化"""
        assert self.picName != None
        # 计算图像的直方图
        imhist, bins = pylab.histogram(self.im.flatten(), 256, normed=True)
        cdf = imhist.cumsum() # 累积分布函数
        cdf = 255 * cdf / cdf[-1] # 归一化
        # 使用累积分布函数的线性插值，计算新的像素值
        im2 = pylab.interp(self.im.flatten(), bins[:-1], cdf)
        self.im = im2.reshape(self.im.shape)

        self.displayImage()

    def btnGaussFilterEvent(self, event):
        dlg = wx.TextEntryDialog(
                self, 'sigma = ',
                '高斯导数滤波器', '5')

        if dlg.ShowModal() == wx.ID_OK:
            self.GaussFilter( float(dlg.GetValue()) )

        dlg.Destroy()

    def GaussFilter(self, sigma):
        """对灰度图进行高斯导数滤波"""
        assert self.picName != None
        imx = pylab.zeros(self.im.shape)
        filters.gaussian_filter(self.im, (sigma, sigma), (0, 1), imx)
        imy = pylab.zeros(self.im.shape)
        filters.gaussian_filter(self.im, (sigma, sigma), (1, 0), imy)
        self.im = pylab.sqrt(imx**2 + imy**2)

        self.displayImage()

    def btnDenoiseEvent(self, event):
        """使用ROF去噪模型对灰度图去噪"""
        assert self.picName != None # 确保已经有图片打开
        self.im, T = rof.denoise(self.im, self.im)
        self.displayImage()

    def btnSaveEvent(self, event):
        """保存最终得到的图片"""
        assert self.picName != None # 确保已经有图片打开
        file_wildcard = "PNG files(*.png)|*.png|All files(*.*)|*.*" 
        dlg = wx.FileDialog(self, 
                            "Save paint as ...",
                            os.getcwd(),
                            style = wx.SAVE | wx.OVERWRITE_PROMPT,
                            wildcard = file_wildcard)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
            if not os.path.splitext(filename)[1]: #如果没有文件名后缀
                filename = filename + '.png'
            from scipy.misc import imsave
            imsave(filename, self.im)
        dlg.Destroy()    

    def btnAboutEvent(self, event):

        dlg = wx.MessageDialog(self, '\t本软件名为《PicProcess》，\t\n为“数字图像处理”课程的大作业。\t\n提供了几种基本的图像处理操作，可组合使用。\
         \n Created by tz二木（qq：3458881709）\n Version 1.0.0 \n 2015-06-28',
                                '关于PicProcess', wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    # 将图像显示在窗口中
    def displayImage(self):
        self.MPL.cla()#必须清理图形,才能显示下一幅图
        self.MPL.imshow(self.im)
        self.MPL.title_MPL(self.picName)
        self.MPL.ShowHelpString("在右侧面板处理图像")
        #self.MPL.grid() 
        self.MPL.UpdatePlot()#必须刷新才能显示

    #（重写函数）打开文件
    def DoOpenFile(self):
        open_dlg = wx.FileDialog(self,message='Choose a file', style=wx.OPEN|wx.CHANGE_DIR)
        if open_dlg.ShowModal() == wx.ID_OK:
            self.picpath=open_dlg.GetPath()
            self.picName = open_dlg.GetFilename()
            try:
                self.im = pylab.array(Image.open(self.picpath).convert('L'))
                self.displayImage()
            except IOError, error:
                dlg = wx.MessageDialog(self, 'Error opening file\n' + str(error))
                dlg.ShowModal()

        open_dlg.Destroy()
     
    
if __name__ == '__main__':  
    app = wx.PySimpleApp()  
    frame = wxMPL_Frame()  
      
    frame.Show()  
    app.MainLoop()  