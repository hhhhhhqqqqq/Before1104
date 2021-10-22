# Untitled - By: admin - 周三 7月 28 2021

#import sensor, image, time

#sensor.reset()
#sensor.set_pixformat(sensor.RGB565)
#sensor.set_framesize(sensor.QVGA)
#sensor.skip_frames(time = 2000)

#clock = time.clock()

#while(True):
    #clock.tick()
    #img = sensor.snapshot()
    #print(clock.fps())



import pyb, sensor, image, time
from pyb import Pin

pin0 = Pin('P0', Pin.IN, Pin.PULL_UP)

#pin1 = Pin('P1', Pin.IN, Pin.PULL_UP)

flag_key1=0
#flag_key2=0


sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

clock = time.clock()

def callback_PIN0(line):
    global flag_key1
    #print("line =", line)
    flag_key1=1
    print("entering the interrupt")
    pyb.delay(10)

#def callback_PIN1(line):
    #global flag_key2
    ##print("line =", line)
    #flag_key2=1
    #pyb.delay(10)


extint = pyb.ExtInt(pin0, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, callback_PIN0)
#extint = pyb.ExtInt(pin1, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, callback_PIN1)

while(True):
    clock.tick()
    img = sensor.snapshot()
    #print(clock.fps())


