#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:SunXiuWen
# make_time:2019/1/15
from django.conf.urls import url
from assets.views import collect_msg

urlpatterns = [
    url(r'report/$', collect_msg.report, name='report')
]
