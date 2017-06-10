__author__ = 'Administrator'

from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^login/',views.login),
    # url(r'^user/',views.user),
    url(r'^register/',views.register, name='register'),
    url(r'^fail_login/',views.fail_login),
    url(r'^family/$',views.family),
    url(r'^doctor/$', views.doctor),
    url(r'^doctor_info/$',views.doctor_info,name='doctor_info'),
    url(r'^manage/',views.manage,name='manage')
]
