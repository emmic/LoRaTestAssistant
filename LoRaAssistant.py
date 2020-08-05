#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import os
import re
import time
import datetime
import winsound
import subprocess
import decimal
import threading
import serial
from tkinter import *
import serial.tools.list_ports
import winsound

window = Tk()
window.title("LoRa测试助手 v1.41(C)")
window.resizable(0,0)
scnWidth,scnHeight = window.maxsize()
width = 520
height = 300
tmpcnf = '%dx%d+%d+%d'%(width, height, (scnWidth-width)/2, (scnHeight-height)/2)
window.geometry(tmpcnf)
rowNum=0
#====================================== MCU选型 =====================================
rowNum= rowNum+1

title0 = Label(window, font=("微软雅黑", 13, "normal"),text = '目标MCU:',anchor='n') 
title0.grid(row=rowNum,column=0)

mcuNum = IntVar()
mcu1 = Radiobutton(window, font=("微软雅黑", 13, "normal"), text="小板子(STM8L)", variable=mcuNum,value=151) 
mcu1.grid(row=rowNum,column=1,sticky=W)
mcu1.select()

mcu2 = Radiobutton(window, font=("微软雅黑", 13, "normal"), text="大板子(STM8S)", variable=mcuNum,value=207) 
mcu2.grid(row=rowNum,column=2,sticky=W)
mcu2.deselect()

#====================================中心频率===================================
rowNum = rowNum+1

freq = IntVar() 
title1 = Label(window, font=("微软雅黑", 13, "normal"),text = '中心频率:',anchor='n') 
title1.grid(row=rowNum,column=0)

Freq433 = Radiobutton(window, font=("微软雅黑", 13, "normal"), text="433MHz", variable=freq,value=433) 
Freq433.grid(row=rowNum,column=1,sticky=W)
Freq433.select()

FreqR1 = Radiobutton(window, font=("微软雅黑", 13, "normal"), text="434MHz", variable=freq,value=434) 
FreqR1.grid(row=rowNum,column=2,sticky=W)
FreqR1.select()

FreqR4 = Radiobutton(window, font=("微软雅黑", 13, "normal"), text="470MHz", variable=freq,value=470) 
FreqR4.grid(row=rowNum,column=3,sticky=W)
FreqR4.deselect()


rowNum = rowNum+1

FreqR2 = Radiobutton(window, font=("微软雅黑", 13, "normal"), text="868MHz", variable=freq,value=868) 
FreqR2.grid(row=rowNum,column=1,sticky=W)
FreqR2.deselect()

FreqR3 = Radiobutton(window, font=("微软雅黑", 13, "normal"), text="915MHz", variable=freq,value=915) 
FreqR3.grid(row=rowNum,column=2,sticky=W)
FreqR3.deselect()


#======================================灵敏度=====================================
rowNum = rowNum+1

title2 = Label(window, font=("微软雅黑", 13, "normal"),text = '灵 敏 度 :',anchor='n') 
title2.grid(row=rowNum,column=0)

sens = IntVar()
Sen1 = Radiobutton(window, font=("微软雅黑", 13, "normal"), text="SF12PL10CR1", variable=sens,value=10) 
Sen1.grid(row=rowNum,column=1,sticky=W)
Sen1.select()

Sen2 = Radiobutton(window, font=("微软雅黑", 13, "normal"), text="SF12PL64CR2", variable=sens,value=64) 
Sen2.grid(row=rowNum,column=2,sticky=W)
Sen2.deselect()


remindMe = IntVar()  
check1 = Checkbutton(window,  font=("微软雅黑", 13, "normal"), text="提示音", variable=remindMe, state='normal')     
check1.grid(row=rowNum,column=3,sticky=W)
check1.select()   


#===================================烧写程序=======================================
rowNum = rowNum+1
downloadRow = rowNum
def SetDownloadInfo(info):
    DownLoadInfoTxt = Label(window, font=("微软雅黑", 13, "normal"),text = info,anchor='n') 
    DownLoadInfoTxt.grid(row=downloadRow,column=3)

def runCmd(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    while p.poll() == None:
        l = p.stdout.readline()
    ret = p.poll()
    return ret

def DownLoader(downloadType):
    disableDownloadBtn()
    if mcuNum.get() == 151:
        mcu="STM8L15xC8"
    if mcuNum.get() == 207:
        mcu="STM8S207CB"
    
  #  mcu="STM8L15xC8"
    SetDownloadInfo('Connect...')
    
    if downloadType == 'RadioPowerTest':
        ProgFile = "POWER_" + mcu + '_' + str(freq.get())+"MHz.hex"

    if downloadType == 'SensityTest':
        if sens.get() == 10:
            ProgFile = "SENS_"+ mcu + '_SF12PL10CR1_' + str(freq.get())+"MHz.hex"
        if sens.get() == 64:
            ProgFile = "SENS_"+ mcu + '_SF12PL64CR2_' + str(freq.get())+"MHz.hex"

    #print (ProgFile)
    if os.path.exists(ProgFile) == False:
        SetDownloadInfo('[File  404]')
        pst2 = PlaySoundThread('wang').start()
        DownLoadBtn2.config(state="disabled")
        return -1
    if os.path.exists(mcu +'-unlock.hex') == False:
        SetDownloadInfo('[File  404]')
        pst2 = PlaySoundThread('wang').start()
        return -1
    SetDownloadInfo('Downloading')

    unlockCmd = 'STVP_CmdLine.exe -BoardName=ST-LINK -Port=USB -ProgMode=SWIM -Device=%s -verif -no_warn_protect -no_loop -no_log -FileOption=%s-unlock.hex' % (mcu, mcu)
    downloadCmd = 'STVP_CmdLine.exe -BoardName=ST-LINK -Port=USB -ProgMode=SWIM -Device=%s -verif -no_log -no_loop -FileProg=%s' % (mcu, ProgFile)
    #print(ProgFile)
    #returnCode = runCmd(unlockCmd)
    returnCode = 0
    #print (unlockCmd)
    if returnCode == 0:
        #SetDownloadInfo('Unlocked √')
        #SetDownloadInfo('[###===]')                                                              
        returnCode = runCmd(downloadCmd)
        if returnCode == 0:
            #SetDownloadInfo('[######]')
            SetDownloadInfo('Download √ ')
            pst1 = PlaySoundThread('done').start()

            
        else:
            #SetDownloadInfo('[###×××]')
            SetDownloadInfo('Download  × ')
            pst2 = PlaySoundThread('wang').start()
    else:
        SetDownloadInfo('Connect ×')
        pst2 = PlaySoundThread('wang').start()
    #time.sleep(6)
    #SetDownloadInfo('[======]')
    enableDownloadBtn();

class newDownloadThread(threading.Thread):
    def __init__(self, downloadType):
        threading.Thread.__init__(self)
        self.downloadType = downloadType
    def run(self):
        DownLoader(self.downloadType)

def downloadTypePower():
    t1 = newDownloadThread('RadioPowerTest')
    t1.start()
    
def downloadTypeSensity():
    t2 = newDownloadThread('SensityTest')
    t2.start()

def disableDownloadBtn():
    DownLoadBtn2.config(state="disabled")
    DownLoadBtn1.config(state="disabled")
def enableDownloadBtn():
    DownLoadBtn2.config(state="normal")
    DownLoadBtn1.config(state="normal")

title3 = Label(window, font=("微软雅黑", 13, "normal"),text = '烧     写 :',anchor='n') 
title3.grid(row=rowNum,column=0)

DownLoadBtn1 = Button(window, font=("微软雅黑", 13, "normal"),text='功率测试程序',width = 14,command=downloadTypePower)
DownLoadBtn1.grid(row=rowNum,column=1)

DownLoadBtn2 = Button(window, font=("微软雅黑", 13, "normal"),text='灵敏度测试程序',width = 14,command=downloadTypeSensity)
DownLoadBtn2.grid(row=rowNum,column=2)



#==================================串口设置========================================
rowNum = rowNum+1
serialRow = rowNum
global ComOpts
ComOpts = []
global com
askStop =False

dingTimes = 0
wangTimes = 0
def SerialConnect():
    cst1=ConnectSerialThread()
    cst1.start()

def SerialDisConnect():
    #com.close()
    global askStop
    if  ComNum.get()[0:3] == 'COM' :
        ConnectBtn['text'] = '请求断开...'
    askStop = True
    
class PlaySoundThread(threading.Thread):
    def __init__(self,type):
        threading.Thread.__init__(self)
        self.type = type
    def run(self):
            global dingTimes
            global wangTimes
            if remindMe.get() == 1:
                   # if wangTimes<=2:
                    if self.type == 'wang':
                            winsound.PlaySound(os.path.abspath('.')+'/wang.wav', winsound.SND_NODEFAULT)
                            wangTimes += 1
                    if self.type == 'done':
                            winsound.PlaySound(os.path.abspath('.')+'/done.wav', winsound.SND_NODEFAULT)
                            wangTimes += 1                    
                    if dingTimes<=1:       
                            if self.type == 'ding':
                                    winsound.PlaySound(os.path.abspath('.')+'/ding.wav', winsound.SND_NODEFAULT)
                                    dingTimes += 1
        
class ConnectSerialThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        if not ComNum.get()[0:3] == 'COM' :
            ConnectBtn['text'] = '无效COM'
        else :
            
                global dataStr
                global lossCount
                global rcvdCount
                global errorCount
                global askStop
                askStop = False
                rcvdCount = 0
                lossCount = 0
                errorCount = 0
                packetLen = 0
                targetLen = 0
                bitCount = 0
                dataStr = ''
                print('尝试连接' + str(ComNum.get()))       
                connectSucess = False
                for times in range(0,50):
                        ConnectBtn['text'] = '连接中...'
                        try:
                                com = serial.Serial(
                                port=ComNum.get(),
                                baudrate= BaudRateVar.get(),
                                parity=serial.PARITY_NONE,
                                stopbits=serial.STOPBITS_ONE,
                                bytesize=serial.EIGHTBITS)
                                print('连接成功！！')
                                connectSucess = True
                        except Exception as e:
                            if times == 50:
                                    ConnectBtn['text'] = '连接失败'
                                    pst1 = PlaySoundThread('wang').start()
                                    askStop = True
                                    print('连接失败! 线程即将终止..')
                                    break
                            time.sleep(0.01) #休息一下
                            
                if connectSucess == True:
                        ConnectBtn['text'] = '连接成功'
                        ConnectBtn['command'] = SerialDisConnect
                        
                        
                ##################下面开始计算误包率####################
                print('开始接收串口数据:')
                correctData = ''
                lastTime = time.time()
                while connectSucess and not askStop :
                        time.sleep(0.01)
                        if com.inWaiting() > 0 :
                                thisTime = time.time()
                                rcvdCount += 1
                                for i in range(0,sens.get() + 2): #除了传输的数据，还有rssi和snr，因此要+2
                                       #有时会收到其他数据，包长比较小，或者串口数据断开了，此处做一个补偿
                                        if com.inWaiting() == 0 :
                                                time.sleep(0.01)
                                                if com.inWaiting() == 0 :#并没有再等到数据
                                                       print ('[' +datetime.datetime.now().strftime('%m-%d %H:%M:%S') +']', end = '')
                                                       print(' %s ' % dataStr)
                                                       dataStr = ''
                                                       lastTime = thisTime
                                                       break
                                        #接收数据，并将十六进制hex数据转为数字
                                        data = ord(com.read(1))
                                        if data < 10: #此处，会将'a'等数变成'0A'
                                               dataStr += '0'+ str(hex(data))[2:].upper() + ' '
                                        else:
                                               dataStr += str(hex(data))[2:].upper() + ' '
                                if len(dataStr) == 3*(sens.get() + 2): #超过长度的直接不管了
                                         print ('[' +datetime.datetime.now().strftime('%m-%d %H:%M:%S') +']', end = '')
                                         print(' %s ' % dataStr)                                        
                                         if sens.get() == 64:
                                                 MaxTimeSpan = 3.8
                                         else :
                                                 MaxTimeSpan = 1.5
                                         correctData = ''
                                         for num in range(0,sens.get()):
                                                 correctData += '00 '
                                                 
                                         while (thisTime - lastTime) > MaxTimeSpan:
                                            #    print('lastTime=%d' ,lastTime)
                                            #    print('thisTime=%d' ,thisTime)                              
                                            #    print(thisTime-lastTime)
                                                lossCount += 1
                                                lastTime += MaxTimeSpan
                                               # print ('[' + time.strftime("%m-%d %H:%M:%S",time.localtime(lastTime)) +']'+'')
                                         if dataStr[:3*(packetLen -2)] != correctData:
                                                errorCount += 1
                                         totalCount = lossCount + rcvdCount
                                         if totalCount !=0:
                                             lossPacketRate = 100* lossCount/totalCount
                                         else:
                                                lossPacketRate = 0

                                         if totalCount !=0:
                                                packetErrorRate = 100* errorCount /totalCount
                                         else:
                                                packetErrorRate = 0
                                                
                                         totalPacketErrorRate = packetErrorRate+lossPacketRate
                                         global PERTxt
                                         global wangTimes
                                         global dingTimes
                                         if totalPacketErrorRate<1:
                                                 if totalCount > 30:
                                                         PERTxt['text'] = str(decimal.Decimal("%.2f" % float(totalPacketErrorRate))) + ' % | 合格'
                                                       #  wangTimes = 0
                                                         pst1 = PlaySoundThread('ding').start()
                                                 else:
                                                         PERTxt['text'] = str(decimal.Decimal("%.2f" % float(totalPacketErrorRate))) + ' % | ???'
                                         else:
                                                # dingTimes = 0
                                              #   pst2 = PlaySoundThread('wang').start()
                                                 PERTxt['text'] = str(decimal.Decimal("%.2f" % float(totalPacketErrorRate))) + ' % | 不合格'

                                         global RSSITxt
                                         rssiValStr = dataStr[3*(packetLen-2):3*(packetLen-2)+2]
                                         rssiVal =  int(rssiValStr, 16)
                                         if rssiValStr[0]>'1':
                                                 rssiVal = rssiVal - 256
                                         RSSITxt['text'] ="RSSI= "+str(rssiVal)  + 'dBm'
                                         global TotalCountTxt
                                         TotalCountTxt['text'] = "总包= " + str(totalCount)
                                         global LossCountTxt
                                         LossCountTxt['text'] = "丢包= " + str(lossCount)+' | ' + str(decimal.Decimal("%.2f" % float(lossPacketRate))) + ' %'
                                         global ErrorCountTxt
                                         ErrorCountTxt['text'] = "错包= "+ str(errorCount)+' | ' + str(decimal.Decimal("%.2f" % float(packetErrorRate))) + ' %'
                                         global SNRTxt
                                         snrValStr =  dataStr[3*(packetLen-1):3*(packetLen-1)+2]
                                         snrVal = int(snrValStr, 16)
                                         if  snrValStr[0]>'3':
                                                 snrVal = snrVal - 256
                                         SNRTxt['text'] = "SNR=  "+ str(snrVal) + 'dB'                                                   

                                         #善后
                                         dataStr = ''
                                         lastTime = thisTime                                        
                #if askStop == True
                ConnectBtn['text'] = '未连接！！'
                ConnectBtn['command'] = SerialConnect
                print('串口监听线程退出！！')                
                        
                            

class FreshAvailableComThread(threading.Thread):
        def __init__(self):
                threading.Thread.__init__(self)
        def run(self):
            global ComOpts
            while True:
                count = 0 #下拉列表更新标志位
                try:
                        port_list = list(serial.tools.list_ports.comports())
                        
                        if len(port_list) == 0:
                                ComOpts=[]
                                if count == 0:
                                        SerialDisConnect()
                                        ComChosen = OptionMenu(window, ComNum, ' ')
                                        ComChosen['width'] = 11
                                        ComNum.set('串口未连接')
                                        ComChosen['font'] = ("微软雅黑", 13, "normal")
                                        ComChosen.grid(row=serialRow,column=1)      # 设置其在界面中出现的位置  column代表列   row 代表行
                                    #    print('串口未连接')
                                        count = 1

                                
                        else:
                            
                                if len(ComOpts) == len(port_list):
                                        for i in range(0,len(port_list)): #检查列表是否需要更新
                                                if not ComOpts[i] == (str(port_list[i])[0:5].replace(' ','')) :
                                                        count += 1
                                else:
                                        if len(ComOpts) == 0 :
                                                count = -1
                                        else:
                                                count = 1
                                
                                if not count == 0 : #需要更新串口下拉菜单
                                        ComOpts=[]
                                        for i in range(0,len(port_list)):
                                                ComOpts.append(str(port_list[i])[0:5].replace(' ',''))
                                                
                                        ComChosen = OptionMenu(window, ComNum, *ComOpts)
                                        if count == -1:
                                                ComNum.set(ComOpts[0])
                                        ComChosen['width'] = 11
                                        ComChosen['font'] = ("微软雅黑", 13, "normal")
                                        ComChosen.grid(row=serialRow,column=1)      # 设置其在界面中出现的位置  column代表列   row 代表行

                except Exception as e:
                        print(e)
                        print('查找串口失败')
                time.sleep(0.1)
                
fact1=FreshAvailableComThread()
fact1.start()


title3 = Label(window, font=("微软雅黑", 13, "normal"),text = '串口设置:',anchor='n') 
title3.grid(row=rowNum,column=0)

ComNum = StringVar()
ComNum.set('请选择串口')
ComChosen =  OptionMenu(window, ComNum,' ')
ComChosen['font'] = ("微软雅黑", 13, "normal")
ComChosen['width'] = 11
ComChosen.grid(row=serialRow,column=1)      # 设置其在界面中出现的位置  column代表列   row 代表行

BaudRateOpts = ['2400','4800','9600','115200']
BaudRateVar = StringVar()
BaudRateVar.set(BaudRateOpts[2])
BaudRate = OptionMenu(window,  BaudRateVar,*BaudRateOpts)
BaudRate['width'] = 11
BaudRate['font'] = ("微软雅黑", 13, "normal")
BaudRate.grid(row=rowNum,column=2)      # 设置其在界面中出现的位置  column代表列   row 代表行

ConnectBtn = Button(window, font=("微软雅黑", 13, "normal"),text="未连接！！",width = 10,command = SerialConnect)
ConnectBtn.grid(row=rowNum,column=3)

#================================灵敏度接收数据统计==================================

rowNum = rowNum+1
'''
class NewEvaluateSensityThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        ConnectBtn['text'] = '停 止'
        ConnectBtn['command'] = StopEvaluateSensity
        init = 0
        rcvdCount = 0
        lossCount = 0
        errorCount = 0
        packetLen = 0
        targetLen = 0
        bitCount = 0
        dataStr = ''
        global com
        global countFlag
        while countFlag :
                time.sleep(0.1)
                if com.inWaiting() > 0 :
                        thisTime = time.time()
                        if init == 1:
                                bitCount = 0
                                for i in range(0,packetLen):
                                       if com.inWaiting() == 0 :
                                               time.sleep(0.3)
                                               if com.inWaiting() == 0 :
                                                       lossCount+=1
                                                       errorCount+=1
                                                       break
                                       data = ord(com.read(1))
                                       bitCount += 1
                                       if data < 10:
                                               dataStr += '0'+ str(hex(data))[2:].upper() + ' '
                                       else:
                                               dataStr += str(hex(data))[2:].upper() + ' '
                        else:
                                packetLen = 0
                                while com.inWaiting() >0:
                                       data = ord(com.read(1))
                                       if data < 10:
                                               dataStr += '0'+ str(hex(data))[2:].upper() + ' '
                                       else:
                                               dataStr += str(hex(data))[2:].upper() + ' '

                                      
                                       packetLen += 1
                       
                        rcvdCount += 1
                if  dataStr != '':               
                        if init == 0 :#未初始化
                                #包长为packetLen-2（最后两个是RSSI and SNR）
                                if packetLen-2 ==64 : #包长为64的情况
                                        MaxTimeSpan = 3.8
                                        lastTime = thisTime
                                        # generate correct data
                                        correctData = ''
                                        for num in range(0,64):
                                                correctData += '00 '
                                        ConnectBtn['text'] = '统计中(64B)'
                                        targetLen = 64
                                        init = 1
                                else:
                                        if packetLen-2 ==10 :#包长为10的情况
                                                MaxTimeSpan = 1.5
                                                lastTime = thisTime
                                                # generate correct data
                                                correctData = ''
                                                for num in range(0,10):
                                                        correctData += '00 '
                                                ConnectBtn['text'] = '统计中(10B)'
                                                targetLen = 10
                                                init = 1
                                        else:
                                                continue
                                                print('packet length not support')
                                                
                        if init == 1 : #已经初始化，开始计算
                                print ('[' +datetime.datetime.now().strftime('%m-%d %H:%M:%S') +']', end = '')
                                print(' %s ' % dataStr)

                                
                             #   print('lastTime=%d' ,lastTime)
                            #    print('thisTime=%d' ,thisTime)           
                                thisTime = time.time()
                                while (thisTime - lastTime) > MaxTimeSpan:
                                    #    print('lastTime=%d' ,lastTime)
                                    #    print('thisTime=%d' ,thisTime)                              
                                    #    print(thisTime-lastTime)
                                        lossCount += 1
                                        lastTime += MaxTimeSpan
                                
                                if not dataStr[:3*(packetLen -2)] == correctData:
                                        errorCount += 1
                                
                                totalCount = lossCount + rcvdCount
                                lossPacketRate = 100* lossCount/totalCount
                                packetErrorRate = 100* errorCount /totalCount
                                totalPacketErrorRate = packetErrorRate+lossPacketRate
                              #  print('totalCount=%d, lossCount=%d, errorCount=%d, packetLen=%d' % (totalCount,lossCount,errorCount, packetLen))
                                #更新控件显示
                                global PERTxt
                                if packetErrorRate<1:
                                        PERTxt['text'] = str(decimal.Decimal("%.2f" % float(totalPacketErrorRate))) + ' % | √'
                                else:
                                        PERTxt['text'] = str(decimal.Decimal("%.2f" % float(totalPacketErrorRate))) + ' % | ×'

                                global RSSITxt
                                rssiValStr = dataStr[3*(packetLen-2):3*(packetLen-2)+2]
                                rssiVal =  int(rssiValStr, 16)
                                if rssiValStr[0]>'1':
                                        rssiVal = rssiVal - 256
                                RSSITxt['text'] ="RSSI= "+str(rssiVal)  + 'dBm'
                                global TotalCountTxt
                                TotalCountTxt['text'] = "总包= " + str(totalCount)
                                global LossCountTxt
                                LossCountTxt['text'] = "丢包= " + str(lossCount)+' | ' + str(decimal.Decimal("%.2f" % float(lossPacketRate))) + ' %'
                                global ErrorCountTxt
                                ErrorCountTxt['text'] = "错包= "+ str(errorCount)+' | ' + str(decimal.Decimal("%.2f" % float(packetErrorRate))) + ' %'
                                global SNRTxt
                                snrValStr =  dataStr[3*(packetLen-1):3*(packetLen-1)+2]
                                snrVal = int(snrValStr, 16)
                                if  snrValStr[0]>'3':
                                        snrVal = snrVal - 256
                                SNRTxt['text'] = "SNR=  "+ str(snrVal) + 'dB'                                                   

                                #善后
                                dataStr = ''
                                lastTime = thisTime
        
                time.sleep(0.4)
'''                        
countFlag = True            
'''
def StartEvaluateSensity():
        est1 = NewEvaluateSensityThread()
        est1.start()
        ConnectBtn['text'] = '开始统计'
        ConnectBtn['command'] = StopEvaluateSensity
def StopEvaluateSensity():
        global com
        com.close()
        ConnectBtn['text'] = '开始统计'
        ConnectBtn['command'] = StartEvaluateSensity
        global countFlag
        countFlag = False
'''
def ClearAll():
        global lossCount
        global rcvdCount
        global errorCount
        global dingTimes
        global wangTimes
        lossCount = 0
        rcvdCount = 0
        errorCount = 0
        totalCount = 0
        lossPacketRate = 0.00
        packetErrorRate = 0.00
        totalPacketErrorRate = 0.00
        dingTimes = 0
        wangTimes = 0
        
        global PERTxt
        PERTxt['text'] = " 0.00"+ ' % |   '
        global RSSITxt
        RSSITxt['text'] ="RSSI= "+'    ' + 'dBm'
        global TotalCountTxt
        TotalCountTxt['text'] = "总包= 0"
        global LossCountTxt
        LossCountTxt['text'] =  "丢包= " +' | ' + '      %'
        global ErrorCountTxt
        ErrorCountTxt['text'] =  "错包= "+' | ' + '      %'
        global SNRTxt
        SNRTxt['text'] = "SNR= "+ '     '+ 'dB'

title4 = Label(window, font=("微软雅黑", 13, "normal"),text = '误 包 率 :',anchor='n') 
title4.grid(row=rowNum,column=0)

PERTxt = Label(window, font=("微软雅黑", 13, "normal"),text =" 0.00"+ ' % |   ', anchor='n') 
PERTxt.grid(row=rowNum,column=1,sticky=N)

RSSITxt = Label(window, font=("微软雅黑", 13, "normal"),text = "RSSI= "+'    ' + 'dBm', anchor='n' ) 
RSSITxt.grid(row=rowNum,column=2,sticky=N)

ClearBtnTxt = "全部清零"
ClearBtn = Button(window, font=("微软雅黑", 13, "normal"),text='全部清零',width = 10,command = ClearAll)
ClearBtn.grid(row=rowNum,column=3,sticky=N)

#=================================================================================
rowNum = rowNum+1

TotalCountTxt = Label(window, font=("微软雅黑", 13, "normal"),text =  "总包= 0" ,anchor='n') 
TotalCountTxt.grid(row=rowNum,column=0,sticky=N)

LossCountTxt = Label(window, font=("微软雅黑", 13, "normal"),text =  "丢包= " +' | ' + '      %',anchor='n') 
LossCountTxt.grid(row=rowNum,column=1,sticky=N)

ErrorCountTxt = Label(window, font=("微软雅黑", 13, "normal"),text = "错包= "+' | ' + '      %', anchor='n') 
ErrorCountTxt.grid(row=rowNum,column=2,sticky=N)

SNRTxt = Label(window, font=("微软雅黑", 13, "normal"),text ="SNR= "+ '     '+ 'dB', anchor='n')
SNRTxt.grid(row=rowNum,column=3,sticky=N)

window.mainloop()
