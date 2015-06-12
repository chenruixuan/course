#!/usr/bin/ python
# encoding: utf-8
# 把str编码由ascii改为utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import recommendations
import wx

class Recommend:
    def __init__(self):
        #userId为数据集中的用户ID，类型为str。maxNum为想要的推荐电影数量。
        self.userId = ''
        self.maxNum = 0
        self.resultList = []
        self.prefs = recommendations.loadMovieLens()

    def startGUI(self):
        app = wx.App()
        win = wx.Frame(None, title = '电影推荐v1.0', size = (750, 600))
        bkg = wx.Panel(win)

        userFilterBtn = wx.Button(bkg, label = '用户过滤')
        userFilterBtn.Bind(wx.EVT_BUTTON, self.recommendByUser)

        itemsFilterBtn = wx.Button(bkg, label = '影片过滤')
        itemsFilterBtn.Bind(wx.EVT_BUTTON, self.recommendByItems)

        userIdLable = wx.StaticText(bkg, -1, '用户ID：')
        self.userIdField = wx.TextCtrl(bkg)
        maxNumLable = wx.StaticText(bkg, -1, '推荐影片数量：')
        self.maxNumField = wx.TextCtrl(bkg)

        # 显示结果的区域
        self.results = wx.TextCtrl(bkg, style = wx.TE_MULTILINE)
        self.results.SetEditable(False)

        hbox = wx.BoxSizer()
        hbox.Add(userIdLable, proportion = 0, flag = wx.EXPAND)
        hbox.Add(self.userIdField, proportion = 1, flag = wx.EXPAND)
        hbox.Add(maxNumLable, proportion = 0, flag = wx.EXPAND)
        hbox.Add(self.maxNumField, proportion = 1, flag = wx.EXPAND)
        hbox.Add(userFilterBtn, proportion = 0, flag = wx.LEFT, border = 5)
        hbox.Add(itemsFilterBtn, proportion = 0, flag = wx.LEFT, border = 5)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(hbox, proportion = 0, flag = wx.EXPAND | wx.ALL, border = 5)
        vbox.Add(self.results, proportion = 1,
                flag = wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, border = 5)

        bkg.SetSizer(vbox)
        win.Show()
        app.MainLoop()

    # 推荐方式一：基于用户的过滤
    def recommendByUser(self, event):
        if not self.isValid(): # 保证输入框存在有效值
            return
        self.resultList = recommendations.getRecommendations(self.prefs,
                self.userId)[0:self.maxNum]
        self.showResult()

    # 推荐方式二：基于影片的过滤
    def recommendByItems(self, event):
        if not self.isValid(): # 保证输入框存在有效值
            return
        itemsim = recommendations.calculateSimilarItems(self.prefs, n = 50)
        self.resultList = recommendations.getRecommendedItems(self.prefs, itemsim,
                self.userId)[0:self.maxNum]
        self.showResult()

    # 输入框有效性验证
    def isValid(self):
        self.userId = self.userIdField.GetValue().strip()
        maxNum = self.maxNumField.GetValue().strip()
        if self.userId == '' or maxNum == '':
            # 报错
            return False
        self.maxNum = int(maxNum)
        return True

    # 将最终结果显示在界面上
    def showResult(self):
        content = '序号\t\t\t预期评分\t\t电影标题\n\n\n'
        i = 0
        for rating, title in self.resultList:
            i += 1
            content += '%04d\t\t\t%.2f\t\t\t%s\n' % (i, rating, title)
        self.results.SetValue(content)


rec = Recommend()
rec.startGUI()
