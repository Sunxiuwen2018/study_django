#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:SunXiuWen
# make_time:2018/11/7
from django.conf.urls import url
from Crm.views import (users, account)

urlpatterns = [
    url(r"login/", account.LoginView.as_view(), name="login"),
    url(r"register/", account.RegisterView.as_view(), name="register"),
    url(r'users/', users.user, name="user_list"),
    url(r'user/add/', users.user, name="user_add"),
    url(r'user/edit/(\d+)/', users.user_add, name="user_edit"),
    url(r'user/del/(\d+)/', users.user_del, name="user_del"),
    url(r'report/', users.report, name="report"),
]
