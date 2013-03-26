from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _
from django.dispatch import receiver
from urllib2 import urlopen
from datetime import datetime, timedelta
from math import sqrt, acos, pi


# Create your models here.
class Device(models.Model):
    name = models.CharField(max_length=100)
    deviceType = models.CharField(max_length=100)
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    address = models.URLField()
    toggleStatus = models.BooleanField()
    onString = models.CharField(max_length=32, default="on")
    offString = models.CharField(max_length=32, default="off")

    def interact(self, inter):
        result = "ERROR: Unknown device type"
        if self.deviceType == "light":
            try:
                opened = urlopen(self.address + (self.offString if self.toggleStatus else self.onString))
                result = "Result from " + opened.geturl() + ": " + opened.read()
                self.toggleStatus = not self.toggleStatus
                self.save()
                inter.complete = True
            except:
                result = "ERROR: Failed resolving URL: " + self.address + (
                self.offString if self.toggleStatus else self.onString)
        elif self.deviceType == "display":
            try:
                last = Interaction.objects.filter(interType="display").latest('timestamp')
            except:
                last = None
            try:
                now = datetime.utcnow()
            except:
                now = None
            try:
                delta = now - last.timestamp
            except BaseException as e:
                delta = None
            if (last is not None) and (not last.complete) and (delta < timedelta(hours=6, seconds=10)):
                try:
                    opened = urlopen(self.address + last.target.name + "&link=cmd://" + self.name)
                    result = "Result from " + opened.geturl() + ": " + opened.read()
                    inter.complete = True
                    inter.save()
                    last.complete = True
                    last.save()
                except:
                    result = "ERROR: Failed resolving URL: " + self.address + self.name + "&link=cmd://" + last.target.name
            else:
                result = "Waiting for second target..."
        return result

    def __unicode__(self):
        return _(u'Device: %(name)s | %(dt)s at %(px)f,%(py)f,%(pz)f') % \
               {'name': self.name,
                'dt': self.deviceType,
                'px': self.x,
                'py': self.y,
                'pz': self.z}


class Sensor(models.Model):
    hwid = models.CharField(max_length=64)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return _(u'Sensor: %(name)s | %(hwid)s') % \
               {'name': self.name,
                'hwid': self.hwid}


class PointGesture(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    px = models.FloatField()
    py = models.FloatField()
    pz = models.FloatField()
    dx = models.FloatField()
    dy = models.FloatField()
    dz = models.FloatField()
    note = models.CharField(max_length=50)

    def __unicode__(self):
        return _(u'Pointed: %(time)s | %(px)f,%(py)f,%(pz)f pointed at %(dx)f,%(dy)f,%(dz)f | %(n)s') % \
               {'time': self.timestamp,
                'px': self.px,
                'py': self.py,
                'pz': self.pz,
                'dx': self.dx,
                'dy': self.dy,
                'dz': self.dz,
                'n': self.note}

    def AngleToDevice(self, t=Device(x=0, y=0, z=0)):
        p2t_x = self.px - t.x
        p2t_y = self.py - t.y
        p2t_z = self.pz - t.z
        p2d_x = self.px - self.dx
        p2d_y = self.py - self.dy
        p2d_z = self.pz - self.dz
        p2t_length = sqrt((p2t_x ** 2) + (p2t_y ** 2) + (p2t_z ** 2))
        p2d_length = sqrt((p2d_x ** 2) + (p2d_y ** 2) + (p2d_z ** 2))

        angle = (p2t_x * p2d_x) + (p2t_y * p2d_y) + (p2t_z * p2d_z)
        angle = angle / (p2t_length * p2d_length)
        angle = acos(angle) * 180 / pi

        return angle


class Interaction(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    target = models.ForeignKey(Device)
    complete = models.BooleanField(default=False)
    result = models.TextField()
    interType = models.CharField(max_length=100)

    def __unicode__(self):
        return _(u'Interaction: %(t)s | %(typ)s %(comp)s, %(res)s') % \
               {'t': self.target.name,
                'comp': "C" if self.complete else "NC",
                'res': self.result,
                'typ': self.interType}


@receiver(models.signals.pre_save, sender=Interaction)
def triggerInteraction(sender, instance, **kwargs):
    if (not instance.complete):
        try:
            instance.result = instance.target.interact(instance)
        except:
            instance.complete = False


@receiver(models.signals.pre_save, sender=PointGesture)
def checkTarget(sender, instance, **kwargs):
    best_angle = 180
    best_target = None
    for t in Device.objects.all():
        t_angle = instance.AngleToDevice(t)
        if t_angle < best_angle:
            best_angle = t_angle
            best_target = t
    instance.note = "No targets." if best_target is None else (
    "" + repr(best_angle) + "deg to " + repr(best_target.name))
    if (best_angle < 30):
        inter = Interaction(target=best_target, interType=best_target.deviceType)
        inter.save()
        instance.note = instance.note + "; Interaction triggered."