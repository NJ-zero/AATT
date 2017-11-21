#coding=utf-8
#author='Shichao-Dong'

import sys
import random,time
import matplotlib
import re,subprocess,os


from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from aatt_pyqt import Ui_Form
import adb_common as adb

class Main(QMainWindow,Ui_Form):

    def __init__(self,parent=None):
        super(Main,self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle('Waiqin365-AATT-V1.0.0')

        self.ui.checkdev.clicked.connect(self.setdevices)
        self.ui.getpackage.clicked.connect(self.setpackage)
        self.ui.cleartext.clicked.connect(self.clearall)
        self.ui.start.clicked.connect(self.startTimer)
        self.ui.end.clicked.connect(self.endTimer)
        #初始化一个定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.slotadd)

        self.ui.comboBox.activated.connect(self.wait_time)

    def setdevices(self):
        '''
        写入设备名
        :return:
        '''
        self.ui.dev.setText(adb.get_devices())

    def setpackage(self):
        '''
        写入package 和 activity
        :return:
        '''
        self.ui.packagename.setText(adb.getpackagename())
        self.ui.activity.setText(adb.getactivity())

    def wait_time(self):
        '''
        设置更新时间
        :return:
        '''
        timetext = self.ui.comboBox.currentText()
        wait_time = int(timetext) * 1000
        print(wait_time)
        return wait_time

    def slotadd(self):
        '''
        往mem、cpu、flow写数据
        :return:
        '''
        memlist = adb.mem()
        mem = 'mem占用：'+ str(memlist[-1])
        cpulist = adb.cpu()
        cpu = 'cpu占用：'+ str(cpulist[-1])
        self.ui.mem.append(mem)
        self.ui.cpu.append(cpu)
        (recevice,send,allflow)=adb.getflow()
        receflow = '下载流量：' + str(int(recevice[-1]/1024))
        sendflow = '上传流量：' + str(int(send[-1]/1024))
        alladd = '总流量：' + str(int(allflow[-1]/1024))
        self.ui.recv.append(receflow)
        self.ui.send.append(sendflow)
        self.ui.all.append(alladd)

    def startTimer(self):
        print(self.ui.comboBox.currentText())
        self.timer.start(self.wait_time())
        self.ui.start.setEnabled(False)
        self.ui.end.setEnabled(True)

    def endTimer(self):
        self.timer.stop()
        self.ui.start.setEnabled(True)

    def clearall(self):
        self.ui.mem.clear()
        self.ui.cpu.clear()
        self.ui.recv.clear()
        self.ui.send.clear()
        self.ui.all.clear()

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    ui = Main()
    ui.show()
    sys.exit(app.exec_())