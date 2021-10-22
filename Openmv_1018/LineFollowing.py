#************************************ (C) COPYRIGHT 2019 ANO ***********************************#
import sensor, image, time, math, struct,lcd
import json
import Message

lcd.init() # Initialize the lcd screen.

#Black_threshold = tuple(Message.list_black.listin)

#Black_threshold =(4, 31, -20, 49, -36, 58)# 寻线 用  黑色
rad_to_angle = 57.29#弧度转度
#一半分别是80和60
IMG_WIDTH = 160
IMG_HEIGHT = 120
# 取样窗口
#冒号前面是key,冒号后面是value,一行是一个item
ROIS = {
    'down':   (0, 105, 160, 15), # 横向取样-下方       1
    'middle': (0, 52,  160, 15), # 横向取样-中间       2
    'up':     (0,  0,  160, 15), # 横向取样-上方       3
    'left':   (0,  0,  15, 120), # 纵向取样-左侧       4
    'right':  (145,0,  15, 120), # 纵向取样-右侧       5
    'All':    (0,  0,  160,120), # 全画面取样-全画面    6
}
class Line(object):
    flag = 0
    color = 0
    angle = 0
    distance = 0
    cross_x=0
    cross_y=0
    cross_flag=0

class LineFlag(object):
    turn_left = 0
    turn_right = 0

LineFlag=LineFlag()
Line=Line()
def CalculateIntersection(line1, line2):

    #a1=dy1, b1=-dx1
    a1 = line1.y2() - line1.y1()
    b1 = line1.x1() - line1.x2()
    c1 = line1.x2()*line1.y1() - line1.x1()*line1.y2()
    img.draw_line((line1.x1(),line1.y1(),line1.x2(),line1.y2()), color=[128,0,128])

    #a2=dy2, b2=-dx2
    a2 = line2.y2() - line2.y1()
    b2 = line2.x1() - line2.x2()
    c2 = line2.x2() * line2.y1() - line2.x1()*line2.y2()
    img.draw_line((line2.x1(),line2.y1(),line2.x2(),line2.y2()), color=[255,255,0])

    #if--slopes are not equal,there would be a cross point
    if (a1 * b2 - a2 * b1) != 0 and (a2 * b1 - a1 * b2) != 0:
        cross_x = int((b1*c2-b2*c1)/(a1*b2-a2*b1))
        cross_y = int((c1*a2-c2*a1)/(a1*b2-a2*b1))

        Line.cross_flag = 1
        Line.cross_x = cross_x-80
        Line.cross_y = cross_y-60
        img.draw_cross(cross_x,cross_y,5,color=[255,0,0])
        return (cross_x, cross_y)
    else:
        Line.cross_flag = 0
        Line.cross_x = 0
        Line.cross_y = 0
        return None
def calculate_angle(line1, line2):
    '''
    利用四边形的角公式， 计算出直线夹角
    '''
    angle  = (180 - abs(line1.theta() - line2.theta()))
    if angle > 90:
        angle = 180 - angle
    return angle

#虽然定义了angle_threshold默认形参值，但当传入实参时，最终运算是按照实参来的(45,90)
def find_interserct_lines(lines, angle_threshold=(10,90), window_size=None):
    '''
    根据夹角阈值寻找两个相互交叉的直线， 且交点需要存在于画面中
    '''
    line_num = len(lines)
    for i in range(line_num -1):
        for j in range(i, line_num):
            # 判断两个直线之间的夹角是否为直角
            angle = calculate_angle(lines[i], lines[j])
            #判断角度差是否在阈值范围内，当角度差不在angle_threshold范围内，continue语句直接跳出，
            #并进行下一次for循环，所以选出来的应该是角度差在(45,90)内的两条直线

            if not(angle >= angle_threshold[0] and angle <=  angle_threshold[1]):
                continue

            # 判断交点是否在画面内
            if window_size is not None:
                # 获取窗口的尺寸 宽度跟高度
                win_width, win_height = window_size
                # 获取直线交点
                intersect_pt = CalculateIntersection(lines[i], lines[j])
                if intersect_pt is None:
                    # 没有交点
                    Line.cross_x = 0
                    Line.cross_y = 0
                    Line.cross_flag = 0
                    continue
                x, y = intersect_pt
                if not(x >= 0 and x < win_width and y >= 0 and y < win_height):
                    # 交点如果没有在画面中
                    Line.cross_x = 0
                    Line.cross_y = 0
                    Line.cross_flag = 0
                    continue
            # 此处返回相交的两条线其实没有起到作用
            return (lines[i], lines[j])
    return None


#寻找每个感兴趣区里的指定色块并判断是否存在
def find_blobs_in_rois(img,colour_threshold):
    '''
    在ROIS中寻找色块，获取ROI中色块的中心区域与是否有色块的信息
    '''
    global ROIS

    roi_blobs_result = {}  # 在各个ROI中寻找色块的结果记录

   #.keys是python的字典函数，返回字典中所有键组成序列，程序开始定义了6个key,如'down''middle'
   # roi_direct=key & roi=value
    for roi_direct in ROIS.keys():#数值复位
        roi_blobs_result[roi_direct] = {
            'cx': -1,
            'cy': -1,
            'blob_flag': False
        }
    for roi_direct, roi in ROIS.items():
        #如果pixels小于pixels_area,色块会被过滤掉
        blobs=img.find_blobs([colour_threshold], roi=roi, merge=True, pixels_area=10)
        if len(blobs) == 0:
            continue
        # 按照元组中pixel的大小排序，并取出最大值
        largest_blob = max(blobs, key=lambda b: b.pixels())

        #blob中有多个值, [:4]表示前四项索引
        #blob[0]=blob.x(), blob[1]=blob.y(), blob[2]=blob.w(), blob[3]=blob.h(),
        #blob[4]=blob.pixels(), blob[5]=blob.cx(), blob[6]=blob.cy()
        x,y,width,height = largest_blob[:4]

        #continue表示不运行循环体剩余部分，而直接进行下次for循环,即continue=跳出当前loop，并进行下一次for循环
        if not(width >=3 and width <= 45 and height >= 3 and height <= 45):
            # 根据色块的长宽进行过滤
            continue


        roi_blobs_result[roi_direct]['cx'] = largest_blob.cx()
        roi_blobs_result[roi_direct]['cy'] = largest_blob.cy()
        #当该区域中找到了blob，返回True
        roi_blobs_result[roi_direct]['blob_flag'] = True
        img.draw_rectangle((x,y,width, height), color=(0,255,255))

    # 判断是否需要左转与右转，这里的左右转包含了90度和非90度的情况
    LineFlag.turn_left = False#先清除标志位
    LineFlag.turn_right = False

    #通过[key],获取dictionary中相应的value值
    if (not roi_blobs_result['up']['blob_flag'] ) and roi_blobs_result['down']['blob_flag'] and roi_blobs_result['left']['blob_flag'] != roi_blobs_result['right']['blob_flag']:
        if roi_blobs_result['left']['blob_flag']:
            LineFlag.turn_left = True
        if roi_blobs_result['right']['blob_flag']:
            LineFlag.turn_right = True
    if (roi_blobs_result['up']['blob_flag']and roi_blobs_result['middle']['blob_flag']and roi_blobs_result['down']['blob_flag']):
        Line.flag = 1#直线
    elif LineFlag.turn_left:
        Line.flag = 2#左转
    elif LineFlag.turn_right:
        Line.flag = 3#右转
    elif (not roi_blobs_result['down']['blob_flag'] ) and roi_blobs_result['up']['blob_flag']and ( roi_blobs_result['right']['blob_flag'] or roi_blobs_result['left']['blob_flag'])and roi_blobs_result['left']['blob_flag'] != roi_blobs_result['right']['blob_flag']:
        Line.flag = 1#左右转后直线
    else:
        Line.flag = 0#未检测到
    #图像上显示检测到的直角类型，是根据LineFlag.turn_x来判断的
    turn_type = 'N' # 啥转角也不是
    if LineFlag.turn_left:
        turn_type = 'L' # 左转
    elif LineFlag.turn_right:
        turn_type = 'R' # 右转
    #img.draw_string(10, 0, 'turn type='+turn_type, color=(255,255,255))


    #计算角度
    CX1 = roi_blobs_result['up']['cx']
    CX2 = roi_blobs_result['middle']['cx']
    #当是直线时候能算distance, 所有情况都能算出角度
    if  Line.flag:
        Line.distance = CX2-80
    else:
        Line.distance = 0
    CX3 = roi_blobs_result['down']['cx']
    CY1 = roi_blobs_result['up']['cy']
    CY2 = roi_blobs_result['middle']['cy']
    CY3 = roi_blobs_result['down']['cy']
    if LineFlag.turn_left or LineFlag.turn_right:
        Line.angle = math.atan((CX2-CX3)/(CY2-CY3))* rad_to_angle
        Line.angle = int(Line.angle)
    elif Line.flag==1 and (roi_blobs_result['down']['blob_flag'] and roi_blobs_result['up']['blob_flag'] ):
        Line.angle = math.atan((CX1-CX3)/(CY1-CY3))* rad_to_angle
        Line.angle = int(Line.angle)
    elif (not roi_blobs_result['down']['blob_flag'] ) and roi_blobs_result['up']['blob_flag']and ( roi_blobs_result['right']['blob_flag'] or roi_blobs_result['left']['blob_flag'])and roi_blobs_result['left']['blob_flag'] != roi_blobs_result['right']['blob_flag']:
        Line.angle = math.atan((CX1-CX2)/(CY1-CY2))* rad_to_angle
        Line.angle = int(Line.angle)
    else:
        Line.angle = 0

    img.draw_string(10, 10, 'angle='+str(Line.angle), color=(255,255,255))
    img.draw_string(10, 25, 'distance='+str(Line.distance), color=(255,255,255))
    lcd.display(img) # Take a picture and display the image.

#线检测
def LineCheck():

    Black_threshold = tuple(Message.list_black.listin)
    print("In line_follwing,Black threshold is ",Black_threshold)

    # 拍摄图片
    global img
    img = sensor.snapshot()
    #theta:角度差，rho半径差,小于阈值就合并为一条直线，在这里已经选择出了需要的单条直线
    lines = img.find_lines(threshold=1000, theta_margin = 50, rho_margin = 50)

    if not lines:
        Line.cross_x=Line.cross_y= Line.cross_flag=0
    # 寻找相交的点 要求满足角度阈值
    # angle_threshold 是两条线的夹角范围
    find_interserct_lines(lines, angle_threshold=(45,90), window_size=(IMG_WIDTH, IMG_HEIGHT))
    #找交线(相差45到90度之间)和找出色块来巡线之间没有任何关系，甚至可以认为找交线这个步骤没有作用
    find_blobs_in_rois(img,Black_threshold)
    #print('交点坐标',Line.cross_x,-Line.cross_y, Line.cross_flag)
    #寻线数据打包发送
    Message.UartSendData(Message.LineDataPack(Line.flag,Line.angle,Line.distance,Line.cross_flag,Line.cross_x,Line.cross_y,Message.Ctr.T_ms))
    return Line.flag

#************************************ (C) COPYRIGHT 2019 ANO ***********************************#
