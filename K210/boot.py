import sensor
import image,ustruct
import lcd,time
import KPU as kpu
import machine
from fpioa_manager import fm
from machine import UART

# need your connect hardware IO 9/10 to loopback
fm.register(9,fm.fpioa.UART2_TX)
fm.register(10,fm.fpioa.UART2_RX)
uart = machine.UART(UART.UART2,baudrate=115200,bits=8,parity=0,stop=1,timeout=1000)


time.sleep_ms(100) # wait uart ready


lcd.init()
lcd.rotation(1)
sensor.reset()
sensor.set_hmirror(0)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((224, 224))

sensor.run(1)
task = kpu.load('/sd/yolo.kmodel')

#classes=[0, 2, 3, 4, 5, 6, 7, 8, 9, 1] #标签名称要和你训练时的标签名称顺序相同
#anchor = (1.8039, 1.8039, 1.9513, 1.9513, 2.0923, 2.0923, 2.2639, 2.2639, 2.4836, 2.4836) #通过K-means聚类算法计算

f=open("anchors.txt","r")
anchor_txt=f.read()
L=[]
for i in anchor_txt.split(","):
    L.append(float(i))
anchor=tuple(L)
f.close()
a = kpu.init_yolo2(task, 0.6, 0.3, 5, anchor)
f=open("lable.txt","r")
labels_txt=f.read()
labels = labels_txt.split(",")
f.close()
position_x=0
position_y=0

#def spi_send(a,a1,a2):
    #'''

    #def line_direct(a:位置,b:时间)

    #'''
    #temp = ustruct.pack("!BBBBhhBB",
                       #0xf9,                       #帧头1
                       #0x09,                       #帧头2
                       #0x05,
                       #int(a),
                       #int(a1), # up sample by 4    #数据1
                       #int(a2),
                       ## up sample by 4    #数据2
                       #0x9d,0xca)
    #print(temp)

    #uart.write(temp)

def NumberDataPack(number,p_x,p_y):

    number_data=bytearray([0xAA,0xFF,0xB1,0x00,int(number)>>8,int(number),p_x>>8,p_x,p_y>>8,p_y,0x00,0x00])
    lens = len(number_data)#数据包大小
    number_data[3] = 6;#有效数据个数
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
        sumcheck = sumcheck+ number_data[i]
        addcheck = addcheck+sumcheck
        i = i+1
    number_data[lens-2] = sumcheck
    number_data[lens-1] = addcheck


    #print(line_data)
    return number_data


def UartSendData(Data):
    uart.write(Data)



while(True):
    img = sensor.snapshot()
    code = kpu.run_yolo2(task, img)
    if code:
        for i in code:
            a=img.draw_rectangle(i.rect(),(0,255,0),2)
            position_x=int(i.x()+i.w()/2)
            position_y=int(i.y()+i.h()/2)
            #position represents central point coordinate
            a=img.draw_cross(position_x,position_y)
            a = lcd.display(img)
            for i in code:
                lcd.draw_string(i.x()+45, i.y()-5, labels[i.classid()]+" "+'%.2f'%i.value(), lcd.WHITE,lcd.GREEN)
            if i.value()>0.5:
                print(labels[i.classid()])
                print(position_x)
                print(i.value())
                #spi_send(labels[i.classid()],position_x,position_y)
                UartSendData(NumberDataPack(labels[i.classid()],position_x,position_y))
                lcd.draw_string(0,0,"re",lcd.WHITE)
            else:
                print("the confidence level is too low")
                UartSendData(NumberDataPack(11,0,0))


    else:
        UartSendData(NumberDataPack(11,0,0))
        a = lcd.display(img)
        #UartSendData(NumberDataPack(11,0,0)



        #spi_send(0xff,00,00)

a = kpu.deinit(task)



