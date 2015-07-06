# course
> 涉及到编程的课程的作业、项目代码。

## network 网络编程

### socket
> Ubuntu下用C进行socket编程。从服务器获取时间，并返回到客户端。

### PosMeasure
>网络编程课的大作业。实验报告参见report.tex。
本项目成品是一个安卓手机APP。它通过扫描多个wifi接入点的信号, 进行一定的处理,近似认为手机的位置就是信号最强AP的位置,从而绘制出自己在地图上的位置。本项目实现了我所在宿舍楼的5个宿舍房间的定位。
实现思路：
1.  接收WiFi无线信号
    通过Andorid系统提供的API,可以得到当前手机连接到的WiFi接入点(AP)的MAC地址和信号强度等信息。由于宿舍区的无线信号种类很多,我进行了一次过滤,只收集名为“seu-wlan”的AP信息,存到一个数组中。然后找到信号强度最好的AP的MAC地址。
2.  得到基本数据
    我到地图中的5个宿舍房间门口进行测试,分别得到一个信号强度最好的AP的MAC地址。把地点和AP的MAC地址对应的信息存储到excel表中。因为宿舍区的WiFi信号特别不稳定,我特意选择了分别位于5个楼层走廊尽头的5个宿舍。
3.  进行测试
    实际使用时,APP会先得到信号最强的AP的MAC地址,然后和excel表中的数据进行比对,找出对应的地点信息。如果没有找到数据记录,则提示错误;如果找到了,则根据地点信息在地图上绘制出手机所在位置。

***
## dataMining 数据挖掘（基于协同过滤算法的电影推荐）
> 参考《集体智慧编程》第2章的算法和示例代码实现。略有改动，使用最新的数据集。使用wxPython做了一个简单的图形化界面。

***
## digitalImageProcess 数字图像处理
> 数字图像处理课程的一些代码。

### picProcess
> 期末大作业。主要使用wxPython和PIL/Matplotlib/Scipy，实现了几个基本的图像处理功能。个人感觉一大难点在于，如何在wxPython中直接显示（嵌入）Matplotlib处理后的图像。写这个软件参考了不少资料。
*存在BUG*: 关闭窗口之后，程序并未退出，还有子进程继续运行。关键在于这行代码：“matplotlib.use("WXAgg")”。因为这个原因，将程序打包为exe之后，多次运行/关闭程序，会产生很多个无用的进程。应该怎么解决呢？
