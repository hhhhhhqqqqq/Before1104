# Untitled - By: hzq - 周日 10月 24 2021

import sensor, image, time, math, ucollections
import Message

one_grid = 50
adjustment = 15


White_threshold=(20, 100, -10, 127, -5, 127)#找白色

#定义类中的二维数组
class Dimension(object):
    x_length=6
    y_length=6



#class NodeSet(object):
    #def


class CoordinInfor(object):
    #def __init__(self,lis,m,n):
        ## self.row=m
        ## self.column=n
        #self.lis=[[0]*n for i in range (m)]
    StartPoint_x=1
    StartPoint_y=1
    EndPoint_x=6
    EndPoint_y=6
    PassableList=[[1,1],[1,2],[2,2],[4,2],[2,3],[3,3],[4,3],[5,3],[3,4],[5,4],[2,5],[3,5],[5,5],[6,5],[6,6],[5,6]]


coordininfor=CoordinInfor([],Dimension.x_length,Dimension.y_length)
#coordininfor.lis[1][1]=9

#print(coordininfor.lis)


class VisitInfor(object):
    def __init__(self,lis,m,n):
        # self.row=m
        # self.column=n
        self.colourlis=[[0]*n for i in range (m)]

visitinfor=VisitInfor([],Dimension.x_length,Dimension.y_length)
#coordininfor.lis[1][1]=9
#sensor.reset()
#sensor.set_pixformat(sensor.RGB565)
#sensor.set_framesize(sensor.QVGA)
#sensor.skip_frames(time = 2000)

#clock = time.clock()

#while(True):
    #clock.tick()
    #img = sensor.snapshot()
    #print(clock.fps())



class Node(object):              #定义所有格子
    def __init__(self,x,y):
        self.passable=0
        self.coordinate=[x,y]
        self.precoordinate=[]
        #self.visit=0
        self.colour=0

class DirectionToSend(object):
    Direction_list=[]

direction= DirectionToSend()

node=[[0]*Dimension.y_length for i in range (Dimension.x_length)]  #m*n two dimension-array -1

# print(node)


i=0
j=0

while i<Dimension.x_length:
    j=0
    while j<Dimension.y_length:
        node[i][j]=Node(i+1,j+1)
        # print(i)
        j=j+1
    i=i+1



def ChangeToPass(list_pass):

    number=len(list_pass)
    print(number)
    l=0
    while (l<number):
        x_index=list_pass[l][0]-1
        y_index=list_pass[l][1]-1
        node[x_index][y_index].passable=1
        l=l+1


def passable(node):
    if coordininfor.lis[node[0]-1][node[0]-1]==1:
        return 1
    else:
        return 0


def checkcolour(node):
    if visitinfor.colourlis[node[0]-1][node[0]-1]==0:
        return 0
    else:
        return 1

def CalculateDirection(pathlist):
    pathlength=len(pathlist)
    #Direction_list=[1]*(pathlength-1)
    q=0
    while q<pathlength-1:
        x_difference=pathlist[q+1][0]-pathlist[q][0]
        y_difference=pathlist[q+1][1]-pathlist[q][1]
        if y_difference == 1:
            direction.Direction_list.append(0)   #0上
        elif x_difference == 1:
            direction.Direction_list.append(1)   #1右
        elif y_difference == -1:
            direction.Direction_list.append(2)   #2下
        elif x_difference == -1:
            direction.Direction_list.append(3)   #3左
        else:
            direction.Direction_list.append(4)   #4出错
        q=q+1
    print("direction_set=",direction.Direction_list)






def bfs():
    search_queue = ucollections.deque((),100)

    route_queue = ucollections.deque((),100)

    #放入初始节点
    start_node=node[coordininfor.StartPoint_x-1][coordininfor.StartPoint_y-1]
    end_node=node[coordininfor.EndPoint_x-1][coordininfor.EndPoint_y-1]

    search_queue.append(start_node)

    route_back = []

    path_back = []

    pathset = []

    path_len = 0

    while search_queue:
        current_node = search_queue.popleft()  #current node 是坐标形式[2,2]
        if current_node.colour==0: #刚弹出的这个节点没有被访问过
            print("current node is",current_node.coordinate)
            if current_node.coordinate!=end_node.coordinate:#刚刚弹出的这个点不是终点
                current_node.colour=1 #设置这个点已经被访问过
                print("current_mode.colour=",current_node.colour)
                #找到相邻节点若没有被访问过，就加入searchqueue
                if Dimension.x_length >= current_node.coordinate[0]-1 >= 1:  #左侧相邻节点
                    left_node = node[current_node.coordinate[0]-2][current_node.coordinate[1]-1]
                    if left_node.passable==1 and left_node.colour==0:
                        search_queue.append(left_node)
                        left_node.precoordinate=current_node.coordinate
                if Dimension.x_length >=current_node.coordinate[0]+1 >=1:  #右侧相邻节点
                    right_node = node[current_node.coordinate[0]][current_node.coordinate[1]-1]
                    if right_node.passable==1 and right_node.colour==0:
                        search_queue.append(right_node)
                        right_node.precoordinate=current_node.coordinate
                if Dimension.y_length >= current_node.coordinate[1]-1 >=1:  #下边相邻节点
                    lower_node = node[current_node.coordinate[0]-1][current_node.coordinate[1]-2]
                    if lower_node.passable==1 and lower_node.colour==0:
                        search_queue.append(lower_node)
                        lower_node.precoordinate=current_node.coordinate
                if Dimension.y_length >= current_node.coordinate[1]+1 >= 1:  #上边相邻节点
                    upper_node = node[current_node.coordinate[0]-1][current_node.coordinate[1]]
                    if upper_node.passable==1 and upper_node.colour==0:
                        search_queue.append(upper_node)
                        upper_node.precoordinate=current_node.coordinate

            else: #刚刚弹出的这个点是终点
                pre_node=current_node
                while(pre_node!=start_node):
                    route_back.append(pre_node)
                    inserted_node=pre_node
                    pre_node_x=inserted_node.precoordinate[0]
                    pre_node_y=inserted_node.precoordinate[1]
                    print("pre_node_x is",pre_node_x)
                    pre_node=node[pre_node_x-1][pre_node_y-1]
                route_back.append(start_node)
                #转换成path_back
                print("route_back[0].coordinate=",route_back[5].coordinate)
                route_length=len(route_back)
                print(route_length)
                p=route_length-1
                #path_back[0]=route_back[0].coordinate
                #print("path_back[0].coordinate=",path_back[0])
                while (p>=0):
                    #test_node=route_back[m]
                    print("p=",p)
                    pathset.append(route_back[p].coordinate)
                    #print("pathset[p]=",path_back[p])
                    p=p-1

                #pathset=path_back.reversed()

                path_length=len(pathset)
                print("pathset=",pathset)
                return(pathset)
                break




#def CaptureWholeMaze(picture_index):
    ##clock.tick()

    #print("Current Exposure == %d" %sensor.get_exposure_us())
    #print("beginning taking photos")

    ##img = sensor.snapshot().gamma_corr(contrast=3)
    #img = sensor.snapshot()
    #img.lens_corr(strength=1.8,zoom=1.0)

    #lines = img.find_lines(threshold=1000, theta_margin = 50, rho_margin = 50)


    #blobs= img.find_blobs([White_threshold], x_stride=5, pixels_threshold=10, area_threshold=10, merge=True)
    #if len(blobs) != 0:
        #a=[blobs[0]]
        #for block in blobs:
            #x,y,width,height,area_pixels = block[:5]
            #if (width >=0 and width <= 200 and height >= 0 and height <= 200 and area_pixels<=30000):
                #a=a+[block]

    ## These values depend on the blob not being circular - otherwise they will be shaky.
    ##print(a[0].pixels())
    ##print("a[0].h=",a[0].h())

        #del a[0]
        #amount_a=len(a)

        #if(amount_a!=0):
            ##print(a)
                ##红灯亮表示找到待选区域
            ##pyb.LED(RED_LED_PIN).on()
            #largest_blob = max(a, key=lambda b: b.pixels())
            #x,y,width,height = largest_blob[:4]

            ## 这些值始终是稳定的。
                ##x_rec,y_rec,w_rec,h_rec = largest_blob.rect()
                ##d_upward = y_rec
                ##d_downward = img.height()-y_rec-h_rec
                ##d_leftward = x_rec
                ##d_rightward = img.width()-x_rec-w_rec

            #img.save("QRcode_pictures/preprocessing_step_1_%d.jpg"%picture_index, quality=95)
            #print("%d preprocesses step1 finished"%picture_index )

            #img.draw_rectangle(largest_blob.rect(), color=127,fill=False)

            #img.save("QRcode_pictures/preprocessing_step_2_%d.jpg"%picture_index, quality=95)
            #print("%d preprocesses step2 finished"%picture_index )

            ##img.draw_cross(largest_blob.cx(), largest_blob.cy(), color=127)
                ### 注意 - 色块的rotation旋转是0-180内的唯一。
            ##img.draw_keypoints([(largest_blob.cx(), largest_blob.cy(), int(math.degrees(largest_blob.rotation())))], size=40, color=127)
                ###print(clock.fps())




            #img_2 = img.copy(roi=(largest_blob.x(),largest_blob.y(),largest_blob.w(),largest_blob.h()))
            #img_2.save("QRcode_pictures/img2_%d.jpg"%picture_index, quality=95)
            #print("%d image_2 first dealt with"%picture_index )
                ##img_2 = img.copy([largest_blob.x(),largest_blob.y(),largest_blob.w(),largest_blob.h()])
                ###img.clear()
                ##img.invert()
                ##if(w_rec>h_rec):
                    ##longer_side = w_rec
                    ##x_start = adjust/2
                    ##length_of_square = longer_side + adjust
                    ##y_start = (length_of_square-h_rec)/2
                    ##img_3 = img.resize(length_of_square,length_of_square)
                    ##img_3.draw_image(img_2,int(x_start),int(y_start))
                    ##img_4 = img_3.invert()
                ##else:
                    ##longer_side = h_rec
                    ##h_start = adjust/2
                    ##length_of_square = longer_side + adjust
                    ##y_start = adjust/2
                    ##x_start = (length_of_square-w_rec)/2
                    ##img_3 = img.resize(length_of_square,length_of_square)
                    ##img_3.draw_image(img_2,int(x_start),int(y_start))
                    ##img_4 = img_3.invert()

                ##lcd.display(img_4,oft=(0,0))
                ##蓝灯亮表示找到二维码，等待一段时间，完成保存
            ##pyb.LED(RED_LED_PIN).off()
            ##pyb.LED(BLUE_LED_PIN).on()
            #lcd.display(img_2,oft=(0,0))
            #print("image 2 has been tooken")
                ##b=img_2.pix_to_ai()
                ##img = img.scale(x_scale=0.5,y_scale=0.5)
                ##lcd.display(img,oft=(0,250))
            #sensor.skip_frames(time = 100)
            #img_2.save("QRcode_pictures/pic_%d.jpg" %picture_index, quality=95)



                ##蓝灯灭表示图片已完成保存
            ##pyb.LED(BLUE_LED_PIN).off()
            #print("Successfully saved picture%d" %picture_index)
            #return 1
        #else:
            #return 0
    #else:
        #return 0


#def WorldCoodinate(object):
    ##find edges of the whole map
    #print("Now is running Surrounding")
    #img = sensor.snapshot()
    #img.lens_corr(strength=1.8,zoom=1.0)
    #blobs= img.find_blobs([colour_threshold], x_stride=10, pixels_threshold=100, area_threshold=5, merge=True)
    #print("len(blobs) is ",len(blobs))
    #for blob in blobs:
         #x,y,width,height= blob[:4]
         #img.draw_rectangle((x,y,width,height), color=(255,255,0))  #黄色


    #if len(blobs) != 0:
        #a=[blobs[0]]
        #for block in blobs:
            #x,y,width,height,area_pixels = block[:5]
            #if (width >=0 and width <= 80 and height >= 0 and height <= 80 and area_pixels<=6400):
                #a=a+[block]
                #img.draw_rectangle((x,y,width,height), color=(255,0,0)) #红色
                #print("a satisfied block has been found")

    ## These values depend on the blob not being circular - otherwise they will be shaky.
    ##print(a[0].pixels())
    ##print("a[0].h=",a[0].h())

        #del a[0]
        #amount_a=len(a)

        #if(amount_a!=0):
            #minimum_distance = 1000000
            #distance_square = 0
            #central_blob=a[0]
            #for block in a:
                #x,y,width,height = block[:4]
                ## img.draw_rectangle((x,y,width, height), color=(0,255,255))
                #distance_square = (block.cx()-80)**2+(block.cy()-60)**2
                ##print("distance_square is",distance_square)
                #if distance_square < minimum_distance:
                    #central_blob = block
                    #minimum_distance=distance_square
                ##print("after every run,minimum distance",minimum_distance)
            #print("after loop, minimun_distance is,",minimum_distance)
            ## the central_blob has alredy been found
            #x_c,y_c,width_c,height_c = central_blob[:4]
            #img.draw_rectangle((x_c,y_c,width_c, height_c), color=(255,255,255))   #白色
            ##central_blob_sole = central_blob
            ##del central_blob
            #state = [0,0,0,0]   #上下左右有没有方框，0代表没有，1代表有
            #for block in a:
                #if one_grid - adjustment < central_blob.cy()-block.cy() < one_grid + adjustment and -adjustment < block.cx()-central_blob.cx() < adjustment:       #上
                    #state[0]=1
                #elif one_grid - adjustment < block.cy()-central_blob.cy() < one_grid + adjustment and -adjustment < block.cx()-central_blob.cx() < adjustment:     #下
                    #state[1]=1
                #elif one_grid - adjustment < central_blob.cx()-block.cx() < one_grid + adjustment and -adjustment < block.cy()-central_blob.cy() < adjustment:     #左
                    #state[2]=1
                #elif one_grid - adjustment< block.cx()-central_blob.cx() < one_grid + adjustment and -adjustment < block.cy()-central_blob.cy() < adjustment:      #右
                    #state[3]=1
            #print(state)
            #return state







#def Plan(object):
ChangeToPass(coordininfor.PassableList)
pathfinal=bfs()
CalculateDirection(pathfinal)
Message.UartSendData(Message.RouteDataPack(direction.Direction_list))











