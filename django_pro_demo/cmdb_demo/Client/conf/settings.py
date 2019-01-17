#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:SunXiuWen
# make_time:2019/1/15
import os

# 远端服务器配置
Params = {
    'server': '192.168.19.17',
    'port': 8000,
    'url': '/assets/report',
    'request_timeout': 30,
}

# 日志文件配置
PATH = os.path.join(os.path.dirname(os.getcwd()), 'log', 'cmdb.log')
