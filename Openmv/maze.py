# Untitled - By: admin - 周五 8月 6 2021

import sensor, image, time, math
import Message

one_grid = 50
adjustment = 15
#sensor.reset()
#sensor.set_pixformat(sensor.RGB565)
#sensor.set_framesize(sensor.QVGA)
#sensor.skip_frames(time = 2000)

#clock = time.clock()

#while(True):
    #clock.tick()
    #img = sensor.snapshot()
    #print(clock.fps())



#1.找到格子
#2.选定中心的格子，判断周边格子的情况

class Coordinate(object):
    CurrentCoordinate=[0,0]
    NextCoordinate=[0,0]

coordinate = Coordinate()

class Direction(object):
    Direction_1=0
    Direction_2=1
    Direction_3=2
    Direction_4=3

Direc = Direction()


class Plane(object):
    Move=1

Plan=Plane()



class Stack(object) :

    def __init__(self,size):
        self.size=size
        self.list=[]   #栈的实现实际上是通过列表的
        self.top=-1
    def push_s(self,ele):  #入栈之前检查栈是否已满
        if self.isfull():
            raise Exception("out of range")        #引发并打印异常，"out of range"
        else:
            self.list.append(ele)
            self.top=self.top+1
    def pop_s(self):             # 出栈之前检查栈是否为空
        if self.isempty():
            raise Exception("stack is empty")
        else:
            self.top=self.top-1
            return self.list.pop()  #python中对于list进行.pop操作，会删除list的最后一个值。并返回该值
    def isfull(self):
        return self.top+1==self.size
    def isempty(self):
        return self.top==-1



stack=Stack(100)

# for i in range(3):    #range(3)表示从0-3,包括0,不包括3
#     stack.push_s(i)
#     # stack.pop_s()

#stack.push_s((1,3))
#stack.push_s((3,4))
#print(stack.list)
# print(stack.isempty())



def Surrounding(colour_threshold):
    print("Now is running Surrounding")
    img = sensor.snapshot()
    img.lens_corr(strength=1.8,zoom=1.0)
    blobs= img.find_blobs([colour_threshold], x_stride=10, pixels_threshold=100, area_threshold=5, merge=True)
    print("len(blobs) is ",len(blobs))
    for blob in blobs:
         x,y,width,height= blob[:4]
         img.draw_rectangle((x,y,width,height), color=(255,255,0))  #黄色


    if len(blobs) != 0:
        a=[blobs[0]]
        for block in blobs:
            x,y,width,height,area_pixels = block[:5]
            if (width >=0 and width <= 80 and height >= 0 and height <= 80 and area_pixels<=6400):
                a=a+[block]
                img.draw_rectangle((x,y,width,height), color=(255,0,0)) #红色
                print("a satisfied block has been found")

    # These values depend on the blob not being circular - otherwise they will be shaky.
    #print(a[0].pixels())
    #print("a[0].h=",a[0].h())

        del a[0]
        amount_a=len(a)

        if(amount_a!=0):
            minimum_distance = 1000000
            distance_square = 0
            central_blob=a[0]
            for block in a:
                x,y,width,height = block[:4]
                # img.draw_rectangle((x,y,width, height), color=(0,255,255))
                distance_square = (block.cx()-80)**2+(block.cy()-60)**2
                #print("distance_square is",distance_square)
                if distance_square < minimum_distance:
                    central_blob = block
                    minimum_distance=distance_square
                #print("after every run,minimum distance",minimum_distance)
            print("after loop, minimun_distance is,",minimum_distance)
            # the central_blob has alredy been found
            x_c,y_c,width_c,height_c = central_blob[:4]
            img.draw_rectangle((x_c,y_c,width_c, height_c), color=(255,255,255))   #白色
            #central_blob_sole = central_blob
            #del central_blob
            state = [0,0,0,0]   #上下左右有没有方框，0代表没有，1代表有
            for block in a:
                if one_grid - adjustment < central_blob.cy()-block.cy() < one_grid + adjustment and -adjustment < block.cx()-central_blob.cx() < adjustment:       #上
                    state[0]=1
                elif one_grid - adjustment < block.cy()-central_blob.cy() < one_grid + adjustment and -adjustment < block.cx()-central_blob.cx() < adjustment:     #下
                    state[1]=1
                elif one_grid - adjustment < central_blob.cx()-block.cx() < one_grid + adjustment and -adjustment < block.cy()-central_blob.cy() < adjustment:     #左
                    state[2]=1
                elif one_grid - adjustment< block.cx()-central_blob.cx() < one_grid + adjustment and -adjustment < block.cy()-central_blob.cy() < adjustment:      #右
                    state[3]=1
            print(state)
            return state


# condition = state & orientation=direction
#def Judge(state,orientation):
    #print(state[2])
    #if orientation==0:
        #if state[2]==1:
            #assump_next = [corrdinate.CurrentCoordinate[0][0]-1,corrdinate.CurrentCoordinate[0][1]]
        #else:
            #return 0
    #elif orientation==1:
        #if state[3]==1:
            #assump_next = [corrdinate.CurrentCoordinate[0][0]+1,corrdinate.CurrentCoordinate[0][1]]
        #else:
            #return 0
    #elif orientation==2:
        #if state[0]==1:
            #assump_next = [corrdinate.CurrentCoordinate[0][0],corrdinate.CurrentCoordinate[0][1]+1]
        #else:
            #return 0
    #elif orientation==3:
        #if state[1]==1:
            #assump_next = [corrdinate.CurrentCoordinate[0][0],corrdinate.CurrentCoordinate[0][1]-1]
        #else:
            #return 0
    #i=0
    #number=len(stack.list)
    #while(i<number):
        #if assump_next == stack.list[i]:
            #return 0
        #i=i+1
    #coordinate.NextCoordinate=assump_next
    #return 1



#def DecisionMaking(state):
    #coordinate.CurrentCoordinate=coordinate.NextCoordinate
    #coordinate.NextCoordinate=[0,0]
    #stack.list.append(coordinate.CurrentCoordinate)  #begin to judge next step after curent position
    #if(Judge(state, Direc.Direction_1)==1):
        #Message.UartSendData(Message.MazeDataPack(state,Direc.Direction_1))
    #elif(Judge(state, Direc.Direction_2)==1):
        #Message.UartSendData(Message.MazeDataPack(state,Direc.Direction_2))
    #elif(Judge(state, Direc.Direction_3)==1):
        #Message.UartSendData(Message.MazeDataPack(state,Direc.Direction_3))
    #elif(Judge(state, Direc.Direction_4)==1):
        #Message.UartSendData(Message.MazeDataPack(state,Direc.Direction_4))






def GoThroughMaze():
    print("has entered module GoThroughMaze")
    White_threshold = tuple(Message.list_white.listin)
    print("In GoThroughMaze,White threshold is ",White_threshold)
    if Plan.Move==1:
        print("Plan.Move==1")
        state_real=Surrounding(White_threshold)
        #print(state_real)
        #DecisionMaking(state_real)



