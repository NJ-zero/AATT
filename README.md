# AATT
## 一款安卓性能测试工具
#### 环境说明
1.windows + python3 + PyQt5
性能数据采集主要基于常用的adb 命令

##### V1.0.0版本说明
主界面如下所示：

![image](https://github.com/NJ-zero/AATT/raw/master/jiemian.png)

点击检查设备---显示设备SN

打开待测应用，获取packagename 和 activity

根据刷新时间定时刷新

点击开始，开始测试，结束，结束测试

后期可优化点：

1.增加弹窗提示

2.增加表格显示

3.设备断开自动停止测试

##### V1.0.2优化
增加关闭和清屏功能

点击关闭，关闭窗口；点击清除，清除写入的mem/cpu/flow等信息