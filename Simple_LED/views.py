from serial import Serial


def light_on(request):
    ser = Serial("/dev/tty.usbserial-A900UCLV", 115200)
    if (not ser.isOpen()):
        ser.open()
    ser.write("m\n9\nW\n")
    text = 'Light is now on.'
    return HttpResponse(text)


def light_off(request):
    ser = Serial("/dev/tty.usbserial-A900UCLV", 115200)
    if (not ser.isOpen()):
        ser.open()
    ser.write("m\n9\nw\n")
    text = 'Light is now off.'
    return HttpResponse(text)