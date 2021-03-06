#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:SunXiuWen
# make_time:2019/1/17
import json
from assets import models


class NewAsset(object):
    def __init__(self, request, data):
        self.request = request
        self.data = data

    def add_to_new_assets_zone(self):
        ram_size = 0
        for x in self.data.get('ram'):
            ram_size += x.get('capacity')

        defaults = {
            'data': json.dumps(self.data),
            'asset_type': self.data.get('asset_type'),
            'manufacturer': self.data.get('manufacturer'),
            'model': self.data.get('model'),
            'ram_size': ram_size,
            'cpu_model': self.data.get('cpu_model'),
            'cpu_count': self.data.get('cpu_core_count'),
            'cpu_core_count': self.data.get('cpu_core_count'),
            'os_distribution': self.data.get('os_distribution'),
            'os_release': self.data.get('os_release'),
            'os_type': self.data.get('os_type')
        }
        # 有就更新，没有就创建
        models.NewAssetApprovalZone.objects.update_or_create(sn=self.data['sn'], defaults=defaults)
        return "资产已经加入或更新待审批区！"
