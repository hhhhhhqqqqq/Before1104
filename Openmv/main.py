#************************************ (C) COPYRIGHT 2019 ANO ***********************************#
import sensor, image, time, math, struct,pyb
import json
from pyb import LED,Timer
from struct import pack, unpack
import Message,CaptureQRcode,QRcode,LineFollowing,Debug,maze
#初始化镜头
sensor.reset()
sensor.set_pixformat(sensor.RGB565)#设置相机模块的像素模式
sensor.set_framesize(sensor.QQVGA)#设置相机分辨率160*120
sensor.skip_frames(time=3000)#时钟
sensor.set_auto_whitebal(False)#若想追踪颜色则关闭白平衡
clock = time.clock()#初始化时钟



#主循环
while(True):
    clock.tick()#时钟初始化
    #接收串口数据
    Message.UartReadBuffer()
    print("Now workmode is",Message.Ctr.WorkMode)
    if Message.Ctr.WorkMode==0: #调试模式
        Debug.SetThreshold()
        #pyb.delay(5000)
    elif Message.Ctr.WorkMode==1: #工作模式
        if Message.Ctr.TaskMode ==1:
            LineFollowing.LineCheck()
    elif Message.Ctr.WorkMode==2: #输入模式
        #lcd.display(maze.Direc.Direction_1,maze.Direc.Direction_2,maze.Direc.Direction_3,maze.Direc.Direction_4)
        print("has already entered mode 2")
        maze.GoThroughMaze()
        pyb.delay(1000)

    #img.binary()
    #if Message.Ctr.WorkMode==1:#点检测
        #DotFollowing.DotCheck()
    #elif (Message.Ctr.WorkMode==2):#线检测
        #LineFollowing.LineCheck()
    #elif Message.Ctr.WorkMode==3:#颜色识别
        #ColorRecognition.ColorRecognition()
    #elif Message.Ctr.WorkMode==4:#二维码识别
        #QRcode.ScanQRcode()
    #elif Message.Ctr.WorkMode==5:#拍照
        #Photography.Photography('IMG.jpg',10)
        #Message.Ctr.WorkMode = LastWorkMode
    #LastWorkMode = Message.Ctr.WorkMode
    #count=1
    #while(count<4):
        #a = 0

        #a = CaptureQRcode.TakeQRcode(count)
        #print("time = %d"%count,"a=%d"%a)
        #count = count+1

    #break
    #CaptureQRcode.TakeQRcode(13)

    #CaptureQRcode.TakeQRcode(14)
    #CaptureQRcode.TakeQRcode(15)
    #break

    #QRcode.ScanQRcode()

    #CaptureQRcode.TakeQRcode(8)
    #CaptureQRcode.TakeQRcode(9)
    #LineFollowing.LineCheck()

    #用户数据发送
    #Message.UartSendData(Message.UserDataPack(127,127,32767,32767,65536,65536,65536,65536,65536,65536))

    ##计算程序运行频率
    #if Message.Ctr.IsDebug == 1:
        #fps=int(clock.fps())
        #Message.Ctr.T_ms = (int)(1000/fps)
        #print('fps',fps,'T_ms',Message.Ctr.T_ms)

#************************************ (C) COPYRIGHT 2019 ANO ***********************************#
