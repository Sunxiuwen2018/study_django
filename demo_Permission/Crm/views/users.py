#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:SunXiuWen
# make_time:2018/11/9
from django.shortcuts import render, reverse,HttpResponse


# Create your views here.

def user(request):
    return render(request, "./user_info/uses_list.html")


def user_add(request):
    pass


def user_edit(request):
    pass


def user_del(request):
    pass


def report(reqeust):
    return HttpResponse("this ok report")
