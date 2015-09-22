### picProcess
> 期末大作业。主要使用wxPython和PIL/Matplotlib/Scipy，实现了几个基本的图像处理功能。个人感觉一大难点在于，如何在wxPython中直接显示（嵌入）Matplotlib处理后的图像。写这个软件参考了不少资料。

> *存在BUG*: 关闭窗口之后，程序并未退出，还有子进程继续运行。关键在于这行代码：`matplotlib.use("WXAgg")`  
因为这个原因，将程序打包为exe之后，多次运行/关闭程序，会产生很多个无用的进程。应该怎么解决呢？
