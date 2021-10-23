# Untitled - By: hzq - 周六 10月 23 2021

import sensor, image, time, lcd
import Message

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

lcd.init()

clock = time.clock()


def DisplayDirection():
    clock.tick()
    img = sensor.snapshot()
    Dir_list=[maze.Direc.Direction_1,maze.Direc.Direction_2,maze.Direc.Direction_3,maze.Direc.Direction_4]
    img.draw_string(5, 5, 'direction='+str(Dir_list), color=(255,255,255))
    lcd.display(img)
