#************************************ (C) COPYRIGHT 2019 ANO ***********************************#
from pyb import UART
#import test
#import LineFollowing
#uart = UART(3,500000)#初始化串口 波特率 500000
uart = UART(3,115200)#初始化串口 波特率 500000

class Receive(object):
    uart_buf = []
    _data_len = 0
    _data_cnt = 0
    state = 0

R=Receive()
# WorkMode=1为寻点模式
# WorkMode=2为寻线模式 包括直线 转角
# WorkMode=3为颜色识别模式
# WorkMode=4为识别二维码模式
# WorkMode=5为拍照模式

class List(object):
    def __init__(self,listin):
        self.listin=[]

list_black = List([])
list_white = List([])

list_black.listin=[4, 31, -20, 49, -36, 58]
list_white.listin=[29, 100, -16, 127, -128, 127]

#print("list_1.listin[0]=",list_1.listin[6])
#print("list_2.listin[0]=",list_2.listin[0])




# ctrl类可以被注释掉
class Ctrl(object):
    #def __init__(self,WorkMode):
        #self.WorkMode = Workmode
    WorkMode = 1    #工作模式
    IsDebug = 1     #不为调试状态时关闭某些图形显示等，有利于提高运行速度
    T_ms = 0
    SetForColour=0
    TaskMode = 1
    Detection = 0
#类的实例化

Ctr=Ctrl()



def UartSendData(Data):
    uart.write(Data)

#串口数据解析
def ReceiveAnl(data_buf,num):
    #和校验
    print("num=",num)
    checksum = 0
    addsum = 0
    i = 0
    while i<(num-2):
        checksum = checksum + data_buf[i]
        addsum = addsum+checksum
        i = i + 1

    checksum = checksum%256 #求余，保留低八位
    addsum = addsum%256
    print("checksum=",checksum)
    print("addsum=",addsum)

    print("data_buf[num-2]=",data_buf[num-2])
    print("data_buf[num-1]=",data_buf[num-1])
    if checksum != data_buf[num-2] or addsum != data_buf[num-1]:
        print("check is not correct")
        return

    # #和校验通过
    # if data_buf[4]==0x00:
    #     Ctr.WorkMode = 0 #调试模式
    #     print("in debug mode Ctr.WorkMode=",Ctr.WorkMode)
    # elif data_buf[4]==0x01: #黑色阈值调整
    #     m=0
    #     while(m<6):
    #         list_black.listin[m]=data_buf[m+5]-0x80
    #         m = m+1
    #     print("list_black.listin=",list_black.listin)
    #     Ctr.SetForColour=1
    # elif data_buf[5]==0x02: #白色阈值调整
    #     l=0
    #     while(l<6):
    #         list_white.listin[l]=data_buf[l+5]-0x80
    #         l = l+1
    #     print("list_white.listin=",list_white.listin)
    #     Ctr.SetForColour=2
    # elif data_buf[4]==0x0A:
    #     Ctr.WorkMode = 1 #工作模式

    if data_buf[2]==0xB2:      #串口屏给openmv调阈值
        if data_buf[4]==0x00:
            Ctr.WorkMode = 0 #调试模式
            print("in debug mode Ctr.WorkMode=",Ctr.WorkMode)
        elif data_buf[4]==0x01: #黑色阈值调整
            m=0
            while(m<6):
                list_black.listin[m]=data_buf[m+5]-0x80
                m = m+1
                print("list_black.listin=",list_black.listin)
                Ctr.SetForColour=1
        elif data_buf[4]==0x02: #白色阈值调整
            l=0
            while(l<6):
                list_white.listin[l]=data_buf[l+5]-0x80
                l = l+1
                print("list_white.listin=",list_white.listin)
                Ctr.SetForColour=2
        elif data_buf[4]==0x0A:
            Ctr.WorkMode = 1 #工作模式

    elif data_buf[2]==0xB4:    #主控控制openmv的taskmode
        if data_buf[4]==0x11:
            Ctr.Taskmode = 1
        elif data_buf[4]==0x12:
            Ctr.Taskmode = 2
        elif data_buf[4]==0x13:
            Ctr.TaskMode = 3

    elif data_buf[2]==0xB5:   #串口屏给openmv输入出口方向
        if data_buf[4]==0x02:
            Ctr.Workmode=2
            maze.Direc.Direction_1=data_buf[5]
            maze.Direc.Direction_2=data_buf[6]
            maze.Direc.Direction_3=data_buf[7]
            maze.Direc.Direction_4=data_buf[8]
        elif data_buf[4]==0x01:
            Ctr.Workmode=1


    elif data_buf[2]==0xB6:   #主控的上一步动作是否完成
        if data_buf[4]==0x01:
            maze.Plan.Move=1
        elif data_buf[4]==0x00:
            maze.Plan.Move=0




#串口通信协议接收
def ReceivePrepare(data):
    if R.state==0 and data==0xAA:    #帧头
        R.state = 1
        R.uart_buf.append(data)
        print("state 1",R.uart_buf)
    elif R.state==1 and data==0xC0:  #目标地址
        R.uart_buf.append(data)
        R.state = 2
    elif R.state==2:                 #功能字
        R.state = 3
        R.uart_buf.append(data)
    elif R.state==3:                #数据个数
        R.state = 4
        R.uart_buf.append(data)
        R._data_len = data
        print("after state 3,buf[]=",R.uart_buf)
    elif R.state==4 and R._data_len > 0:      #有效数据
        R._data_len = R._data_len-1
        R.uart_buf.append(data)
        if R._data_len ==0 :
            print("after state4, buf[]=",R.uart_buf)
            R.state = 5
    elif R.state==5:                          #校验和
        R.state = 6
        R.uart_buf.append(data)
    elif R.state==6:                          #附加和
        R.state = 0
        R.uart_buf.append(data)
        print("the received data_buf=",R.uart_buf)
        print("R.uart_buf[3]+6",R.uart_buf[3]+6)
        ReceiveAnl(R.uart_buf,R.uart_buf[3]+6)
        R.uart_buf=[]#清空缓冲区，准备下次接收数据
        R._data_len=0 #恢复初始值
    else:
        R.state = 0




# void UserTask_ReceiveData(u8 received_data){
#     static u8 _data_len = 0,_data_cnt = 0;
#     static u8 rxstate = 0;

# 	if(rxstate == 0 && received_data == 0xAA)
# 	//HEAD
#     {
# 		rxstate = 1;
# 		_datatemp[0] = received_data;
# 	}
# 	else if(rxstate == 1)
# 	//Dest
#     {
# 		rxstate = 2;
# 		_datatemp[1] = received_data;
# 	}
# 	else if(rxstate == 2)
#     //Func
# 	{
# 		rxstate = 3;
# 		_datatemp[2] = received_data;
# 	}
# 	else if(rxstate == 3 && received_data < 250)
#     //Len
# 	{
# 		rxstate = 4;
# 		_datatemp[3] = received_data;
# 		_data_len = received_data;
# 		_data_cnt = 0;
# 	}
# 	else if(rxstate == 4 && _data_len > 0)
#     //Data
# 	{
# 		_data_len--;
# 		_datatemp[4+_data_cnt++] = received_data;
# 		if(_data_len == 0)
# 			rxstate = 5;
# 	}
# 	else if(rxstate == 5)
#     //Sumcheck
# 	{
# 		rxstate = 6;
# 		_datatemp[4+_data_cnt++] = received_data;
# 	}
# 	else if(rxstate==6)
# 	//Add on check
#     {
# 		rxstate = 0;
# 		_datatemp[4+_data_cnt] = received_data;
#         //UserTask_FC_SendData(_datatemp, _data_cnt + 5);
#         if (_datatemp[1] == HW_OPENMV)
#         {
#             UserTask_OpenMV_SendData(_datatemp, _data_cnt + 5);
#         }
#         else if (_datatemp[1] == HW_K210)
#         {
#             UserTask_K210_SendData(_datatemp, _data_cnt + 5);
#         }
#         else if (_datatemp[1] == HW_ALL)
#         {
#             UserTask_FC_SendData(_datatemp, _data_cnt + 5);
#         }
#         else
#         {
#             UserTask_URATScreen_CombineData(_datatemp);
#         }

# 	}
# 	else
# 	{
# 		rxstate = 0;
# 	}

#     // u8 text1[30];
#     // sprintf(text1,"t4.txt=\"here\"");
#     // UserTask_URATScreen_SendData(text1);
# }




#读取串口缓存
def UartReadBuffer():
    #print("enter")
    i = 0
    Buffer_size = uart.any()
    #print("Buffer_size=",Buffer_size)
    while i<Buffer_size:
        ReceivePrepare(uart.readchar())
        i = i + 1

##点检测数据打包
#def DotDataPack(color,flag,x,y,T_ms):
    #print("found: x=",x,"  y=",-y)
    #pack_data=bytearray([0xAA,0x29,0x05,0x41,0x00,color,flag,x>>8,x,(-y)>>8,(-y),T_ms,0x00])
    #lens = len(pack_data)#数据包大小
    #pack_data[4] = 7;#有效数据个数
    #i = 0
    #sum = 0
    ##和校验
    #while i<(lens-1):
        #sum = sum + pack_data[i]
        #i = i+1
    #pack_data[lens-1] = sum;
    #return pack_data

#线检测数据打包
def LineDataPack(flag,angle,distance,crossflag,crossx,crossy,T_ms):
    if (flag == 0):
        print("found: angle",angle,"  distance=",distance,"   线状态   未检测到直线")
    elif (flag == 1):
        print("found: angle",angle,"  distance=",distance,"   线状态   直线")
    elif (flag == 2):
        print("found: angle",angle,"  distance=",distance,"   线状态   左转")
    elif (flag == 3):
        print("found: angle",angle,"  distance=",distance,"   线状态   右转")

    line_data=bytearray([0xAA,0xFF,0xB0,0x00,flag,angle>>8,angle,distance>>8,distance,crossflag,crossx>>8,crossx,(-crossy)>>8,(-crossy),T_ms,0x00,0x00])
    lens = len(line_data)#数据包大小
    line_data[3] = 11;#有效数据个数
    i = 0
    sumcheck = 0
    addcheck = 0

    #和校验
    #while i<(lens-1):
    #    sum = sum + line_data[i]
    #    i = i+1
    #line_data[lens-1] = sum;

    #校验方式2
    while i<(lens-2):
        sumcheck = sumcheck+ line_data[i]
        addcheck = addcheck+sumcheck
        i = i+1
    line_data[lens-2] = sumcheck
    line_data[lens-1] = addcheck


    #print(line_data)
    return line_data

def MazeDataPack(flag, orientation):
    if(flag==0):
        print("has already reached destination")
    if(flag==1):
        print("continuing move")


    maze_data=bytearray([0xAA,0xFF,0xB7,0x00,flag,orientation,0x00,0x00])
    lens = len(maze_data)#数据包大小
    maze_data[2] = 11;#有效数据个数
    i = 0
    sumcheck = 0
    addcheck = 0

    #和校验
    #while i<(lens-1):
    #    sum = sum + line_data[i]
    #    i = i+1
    #line_data[lens-1] = sum;

    #校验方式2
    while i<(lens-2):
        sumcheck = sumcheck+ line_data[i]
        addcheck = addcheck+sumcheck
        i = i+1
    maze_data[lens-2] = sumcheck
    maze_data[lens-1] = addcheck


    #print(line_data)
    return maze_data


##用户数据打包
#def UserDataPack(data0,data1,data2,data3,data4,data5,data6,data7,data8,data9):
    #UserData=bytearray([0xAA,0x05,0xAF,0xF1,0x00
                        #,data0,data1,data2>>8,data2,data3>>8,data3
                        #,data4>>24,data4>>16,data4>>8,data4
                        #,data5>>24,data5>>16,data5>>8,data5
                        #,data6>>24,data6>>16,data6>>8,data6
                        #,data7>>24,data7>>16,data7>>8,data7
                        #,data8>>24,data8>>16,data8>>8,data8
                        #,data9>>24,data9>>16,data9>>8,data9
                        #,0x00])
    #lens = len(UserData)#数据包大小
    #UserData[4] = lens-6;#有效数据个数
    #i = 0
    #sum = 0
    ##和校验
    #while i<(lens-1):
        #sum = sum + UserData[i]
        #i = i+1
    #UserData[lens-1] = sum;
    #return UserData

#************************************ (C) COPYRIGHT 2019 ANO ***********************************#
