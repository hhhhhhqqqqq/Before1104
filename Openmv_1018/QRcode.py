import sensor, image,Message,lcd

class QRcode(object):
    QRcodemessage=0

QRcode=QRcode()
def ScanQRcode():
    img = sensor.snapshot()
    img.lens_corr(strength=1.8,zoom=1.0)
    print("enter")
    for code in img.find_qrcodes():
        print(code)
        img.draw_rectangle(code.rect(), color = 255)
        img.save("QRcode_pictures/test_0.jpg", quality=95)
        QRcode.QRcodemessage=1
        print('信息',code.payload())
        return code.payload()
    #if QRcode.QRcodemessage:
        #二维码识别数据打包发送
        #Message.UartSendData(Message.QRcodeDataPack(QRcode.QRcodemessage,Message.Ctr.T_ms))
