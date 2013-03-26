# Create your views here.
from django.http import HttpResponse
from models import *
from serial import Serial


def get_sensor_name(request):
    try:
        text = Sensor.objects.get(hwid=request.GET.get('id', '')).name
    except Sensor.DoesNotExist:
        Sensor.objects.create(hwid=request.GET.get('id', ''), name='NewSensor')
        text = 'NewSensor'
    return HttpResponse(text)


def trigger_point_gesture(request):
    PointGesture.objects.create(px=float(request.GET.get('px', 0.0)), py=float(request.GET.get('py', 0.0)),
                                pz=float(request.GET.get('pz', 0.0)),
                                dx=float(request.GET.get('dx', 0.0)), dy=float(request.GET.get('dy', 0.0)),
                                dz=float(request.GET.get('dz', 0.0)))
    text = 'New point gesture accepted.'
    return HttpResponse(text)


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