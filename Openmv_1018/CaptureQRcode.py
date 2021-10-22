
import sensor,image,lcd,time,math,pyb,os

import Message

#lcd.init()
#sensor.reset()
#sensor.set_pixformat(sensor.RGB565)
#sensor.set_framesize(sensor.QVGA)
#sensor.set_windowing((224, 224))	#set to 224x224 input
#sensor.set_hmirror(1)				#flip camera kz15的板子需要
##sensor.skip_frames(time = 3000)
#sensor.set_auto_gain(False) # 颜色跟踪必须关闭自动增益
#sensor.set_auto_whitebal(False) # 颜色跟踪必须关闭白平衡

#lcd.rotation(1)

#clock = time.clock()

#QR_threshold =(0, 55, -128, 127, -128, 127) #找黑色


#sensor.set_auto_exposure(False, \
    #exposure_us = 18000)

#sensor.skip_frames(time = 8000)


QR_threshold =(20, 100, -10, 127, -5, 127)#找白色

adjust = 10

RED_LED_PIN = 1
BLUE_LED_PIN = 3

class CaptureQRcode(object):
    CaptureQRcodemessage=0

CaptureQRcode=CaptureQRcode()





def TakeQRcode(picture_index):
    #clock.tick()

    print("Current Exposure == %d" %sensor.get_exposure_us())
    print("beginning taking photos")

    #img = sensor.snapshot().gamma_corr(contrast=3)
    img = sensor.snapshot()
    img.lens_corr(strength=1.8,zoom=1.0)

    blobs= img.find_blobs([QR_threshold], x_stride=5, pixels_threshold=10, area_threshold=10, merge=True)
    if len(blobs) != 0:
        a=[blobs[0]]
        for block in blobs:
            x,y,width,height,area_pixels = block[:5]
            if (width >=0 and width <= 200 and height >= 0 and height <= 200 and area_pixels<=30000):
                a=a+[block]

    # These values depend on the blob not being circular - otherwise they will be shaky.
    #print(a[0].pixels())
    #print("a[0].h=",a[0].h())

        del a[0]
        amount_a=len(a)

        if(amount_a!=0):
            #print(a)
                #红灯亮表示找到待选区域
            #pyb.LED(RED_LED_PIN).on()
            largest_blob = max(a, key=lambda b: b.pixels())
            x,y,width,height = largest_blob[:4]

            # 这些值始终是稳定的。
                #x_rec,y_rec,w_rec,h_rec = largest_blob.rect()
                #d_upward = y_rec
                #d_downward = img.height()-y_rec-h_rec
                #d_leftward = x_rec
                #d_rightward = img.width()-x_rec-w_rec

            img.save("QRcode_pictures/preprocessing_step_1_%d.jpg"%picture_index, quality=95)
            print("%d preprocesses step1 finished"%picture_index )

            img.draw_rectangle(largest_blob.rect(), color=127,fill=False)

            img.save("QRcode_pictures/preprocessing_step_2_%d.jpg"%picture_index, quality=95)
            print("%d preprocesses step2 finished"%picture_index )

            #img.draw_cross(largest_blob.cx(), largest_blob.cy(), color=127)
                ## 注意 - 色块的rotation旋转是0-180内的唯一。
            #img.draw_keypoints([(largest_blob.cx(), largest_blob.cy(), int(math.degrees(largest_blob.rotation())))], size=40, color=127)
                ##print(clock.fps())




            img_2 = img.copy(roi=(largest_blob.x(),largest_blob.y(),largest_blob.w(),largest_blob.h()))
            img_2.save("QRcode_pictures/img2_%d.jpg"%picture_index, quality=95)
            print("%d image_2 first dealt with"%picture_index )
                #img_2 = img.copy([largest_blob.x(),largest_blob.y(),largest_blob.w(),largest_blob.h()])
                ##img.clear()
                #img.invert()
                #if(w_rec>h_rec):
                    #longer_side = w_rec
                    #x_start = adjust/2
                    #length_of_square = longer_side + adjust
                    #y_start = (length_of_square-h_rec)/2
                    #img_3 = img.resize(length_of_square,length_of_square)
                    #img_3.draw_image(img_2,int(x_start),int(y_start))
                    #img_4 = img_3.invert()
                #else:
                    #longer_side = h_rec
                    #h_start = adjust/2
                    #length_of_square = longer_side + adjust
                    #y_start = adjust/2
                    #x_start = (length_of_square-w_rec)/2
                    #img_3 = img.resize(length_of_square,length_of_square)
                    #img_3.draw_image(img_2,int(x_start),int(y_start))
                    #img_4 = img_3.invert()

                #lcd.display(img_4,oft=(0,0))
                #蓝灯亮表示找到二维码，等待一段时间，完成保存
            #pyb.LED(RED_LED_PIN).off()
            #pyb.LED(BLUE_LED_PIN).on()
            lcd.display(img_2,oft=(0,0))
            print("image 2 has been tooken")
                #b=img_2.pix_to_ai()
                #img = img.scale(x_scale=0.5,y_scale=0.5)
                #lcd.display(img,oft=(0,250))
            sensor.skip_frames(time = 100)
            img_2.save("QRcode_pictures/pic_%d.jpg" %picture_index, quality=95)



                #蓝灯灭表示图片已完成保存
            #pyb.LED(BLUE_LED_PIN).off()
            print("Successfully saved picture%d" %picture_index)
            return 1
        else:
            return 0
    else:
        return 0







    #img = sensor.snapshot()
    #img.lens_corr(strength=1.8,zoom=1.0)
    #print("enter")
    #for code in img.find_qrcodes():
        #print(code)
        #img.draw_rectangle(code.rect(), color = 255)
        #CaptureQRcode.CaptureQRcodemessage=1
        #print('信息',code.payload())
        #return code.payload()
    #if QRcode.QRcodemessage:
        #二维码识别数据打包发送
        #Message.UartSendData(Message.QRcodeDataPack(QRcode.QRcodemessage,Message.Ctr.T_ms))



