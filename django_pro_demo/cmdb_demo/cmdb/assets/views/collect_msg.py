#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:SunXiuWen
# make_time:2019/1/16
import json

from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from assets import models

from . import asset_handler

@csrf_exempt
def report(request):
    if request.method == 'POST':
        asset_data = request.POST.get('asset_data')  # 收到的是一个json字典
        print(asset_data)
        data = json.loads(asset_data)
        # 各种数据检查，请自行添加和完善
        if not data:
            return HttpResponse("没有数据！")
        if not issubclass(dict, type(data)):
            return HttpResponse("数据必须为字典格式！")
        # 是否携带了关键的sn号
        sn = data.get('sn', None)
        if sn:
            # 进入审批流程
            # 首先判断是否在上线资产中存在该sn
            asset_obj = models.Asset.objects.filter(sn=sn)
            if asset_obj:
                # 进入已上线资产的数据更新流程
                pass
                return HttpResponse("资产数据已经更新！")
            else:  # 如果已上线资产中没有，那么说明是未批准资产，进入新资产待审批区，更新或者创建资产
                obj = asset_handler.NewAsset(request, data)
                response = obj.add_to_new_assets_zone()
                return HttpResponse(response)
        else:
            return HttpResponse("没有资产sn序列号，请检查数据！")
    return HttpResponse("可以不加斜杠")
