# Untitled - By: hzq - 周四 10月 28 2021

import sensor, image, time, ucollections

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

clock = time.clock()

#while(True):
    #clock.tick()
    #img = sensor.snapshot()
    #print(clock.fps())

liste = ucollections.deque(NULL,100)
liste.append(1)
print(liste[0])
