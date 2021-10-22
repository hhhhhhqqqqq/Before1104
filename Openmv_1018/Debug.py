# Untitled - By: admin - 周五 7月 30 2021

import sensor, image, time, lcd
import Message

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

lcd.init()

clock = time.clock()


def SetThreshold():
    clock.tick()
    img = sensor.snapshot()

    if Message.Ctr.SetForColour==1:
        Black_threshold = tuple(Message.list_black.listin)
        print("In Debug,Black threshold is ",Black_threshold)
        img.binary([Black_threshold])
        img.draw_string(5, 5, 'th='+str(Black_threshold), color=(255,255,255))
        lcd.display(img)
    elif Message.Ctr.SetForColour==2:
        White_threshold = tuple(Message.list_white.listin)
        print("In Debug,White threshold is ",White_threshold)
        img.binary([White_threshold])
        img.draw_string(5, 5, 'th='+str(white_threshold), color=(255,255,255))
        lcd.display(img)

    #print(clock.fps())
