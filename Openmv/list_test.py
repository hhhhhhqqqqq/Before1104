# Untitled - By: admin - 周四 7月 29 2021

import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

clock = time.clock()



class List(object):
    def __init__(self,listin):
        self.listin=[]


list_1 = List([0])
list_2 = List([0])
list_1.listin=[1,2]
list_2.listin=[3,4]
print("list_1.listin[0]=",list_1.listin[0])
print("list_2.listin[0]=",list_2.listin[0])



#while(True):
    #clock.tick()
    #img = sensor.snapshot()
    #print(clock.fps())
