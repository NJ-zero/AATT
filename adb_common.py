#coding=utf-8
#author='Shichao-Dong'

import os,platform
import subprocess
import re


si = subprocess.STARTUPINFO()
si.dwFlags |= subprocess.STARTF_USESHOWWINDOW

dev_list =[]
def get_devices():
    # rt = os.popen('adb devices').readlines()  # os.popen()执行系统命令并返回执行后的结果
    # n = len(rt) - 2
    # print(rt)
    # print("当前已连接待测手机数为：" + str(n))
    # if len(rt)-2 == 1:
    #     for i in range(n):
    #         nPos = rt[i + 1].index("\t")
    #         dev = rt[i + 1][:nPos]
    #         dev_list.append(dev)
    #         print(dev_list[0])
    #     return dev_list[0]
    # else:
    #     return 'No device found'
    devices = []
    result = subprocess.Popen("adb devices", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.readlines()
    # print(result[1].decode())
    print(len(result))
    if len(result)-2 == 1:
        for line in result[1:]:
            devices.append(line.strip().decode())
        print(devices[0].split()[0])
        return devices[0].split()[0]
    else:
        print('No device')
        return 'No device found'


    # return devices[0]


def getpackagename():
    pattern = re.compile(r"[a-zA-Z0-9\.]+/.[a-zA-Z0-9\.]+")
    package = subprocess.Popen("adb shell dumpsys activity | findstr  mFocusedActivity", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.read()
    package =  (str(package))
    packagename = pattern.findall(package)[0].split('/')[0]
    # print (pattern.findall(package)[0].split('/')[0])
    # print (pattern.findall(package)[0].split('/')[1])
    return packagename

def getactivity():
    pattern = re.compile(r"[a-zA-Z0-9\.]+/.[a-zA-Z0-9\.]+")
    package = subprocess.Popen("adb shell dumpsys activity | findstr  mFocusedActivity", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.read()
    package =  (str(package))
    activity = pattern.findall(package)[0].split('/')[1]
    return activity


#获取mem占用情况
mem_list = []
def mem():
    cmd = 'adb -s '+ get_devices() + ' shell dumpsys meminfo ' + getpackagename()
    men_s = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.readlines()
    for info in men_s:
        if len(info.split())>0 and info.split()[0].decode() == "TOTAL":
            mem_list.append((int(info.split()[1].decode())//1024))
            print(str(info.split()[1].decode()))
            print(mem_list)
            # men_list = str(info.split()[1].decode())

    return mem_list

#获取cpu
cpu_list=[]
def cpu():
    cmd = 'adb -s '+get_devices() + ' shell top -n 1| findstr ' + getpackagename()
    # print (cmd)
    top_info = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.readlines()
    print (top_info)
    if len(top_info)>=1:
        cpu_list.append(int(top_info[0].split()[2][0:-1]))

    print (cpu_list)

    return cpu_list

#获取pid和uid
pid_list = []
def pid():
    cmd = 'adb -s '+ get_devices() +' shell ps |findstr ' + getpackagename()
    print (cmd)
    pid_info = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.readlines()
    print(int(pid_info[0].split()[1]))

    if len(pid_info)>=1:
        pid_list.append(int(pid_info[0].split()[1]))
        print(pid_list)
    return str(pid_list[0])

uid_list = []
def uid():
    cmd ='adb -s '+ get_devices() +' shell cat  /proc/'+ pid() + '/status'
    print (cmd)
    uid_info = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.readlines()
    if len(uid_info)>= 1:
        uid_list.append(int(uid_info[6].split()[1]))
        print (uid_list)
    return str(uid_list[0])

#获取流量
receive = []
sendflow = []
all = []
def flow():
    cmd = 'adb -s '+ get_devices() +' shell cat /proc/net/xt_qtaguid/stats | findstr '+ uid()
    print (cmd)
    flow_info = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.readlines()
    down = 0
    up = 0
    if len(flow_info)>= 1:
        for flow in flow_info:
            down =down + int(flow.split()[5])
            up = up+ int(flow.split()[7])
        receive.append(down)
        sendflow.append(up)
    print (receive,sendflow)
    return (receive,sendflow)


def getflow():
    (receive,sendflow) = flow()
    recev = []
    send = []
    allflow = []
    print(len(receive))
    for i in range(len(receive)-1):
        recev.append((int(receive[i+1]) - int(receive[i]))//1024)
        send.append((int(sendflow[i+1]) - int(sendflow[i]))//1024)
        allflow.append(recev[i]+send[i])
    print(recev,send,allflow)
    return recev,send,allflow




if __name__ == "__main__":
    get_devices()
    getpackagename()
    mem()
    # cpu()
    # pid()
    # uid()

    # for i in range(20):
    #     flow()

    # getflow()