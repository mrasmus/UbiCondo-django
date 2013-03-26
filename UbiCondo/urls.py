from django.conf.urls import patterns, include, url
from MainControl.models import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()
admin.site.register(Sensor)
admin.site.register(Device)
admin.site.register(PointGesture)
admin.site.register(Interaction)

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'UbiCondo.views.home', name='home'),
                       # url(r'^UbiCondo/', include('UbiCondo.foo.urls')),

                       # Uncomment the admin/doc line below to enable admin documentation:
                       url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),

                       url(r'^sensor/register', 'MainControl.views.get_sensor_name'),
                       url(r'^sensor/pointgesture', 'MainControl.views.trigger_point_gesture'),
                       url(r'^light/on', 'MainControl.views.light_on'),
                       url(r'^light/off', 'MainControl.views.light_off'),
)
