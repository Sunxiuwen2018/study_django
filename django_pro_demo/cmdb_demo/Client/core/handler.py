#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:SunXiuWen
# make_time:2019/1/15
import json
import time
# import urllib.parse
# import urllib.request
import requests
from core import info_collection
from conf import settings

import sys

if sys.version_info.major != 3:
    # py2中可以使用下面的
    reload(sys)
    sys.setdefaultencoding('utf8')


class ArgvHandler(object):
    def __init__(self, args):
        self.args = args
        self.parse_args()

    def parse_args(self):
        """
        分析参数，如果有参数指定的功能，则执行该功能，如果没有，打印帮助说明
        :return:
        """
        if len(self.args) > 1 and hasattr(self, self.args[1]):
            func = getattr(self, self.args[1])
            func()
        else:
            self.help_msg()

    @staticmethod
    def help_msg():
        """帮助说明"""
        msg = """
        collect_data  收集硬件信息
        report_data   收集硬件信息并汇报
        """
        print(msg)

    @staticmethod
    def collect_data():
        """收集硬件信息，用于测试"""
        info = info_collection.InfoCollection()
        asset_data = info.collect()
        print(asset_data)

    @staticmethod
    def report_data():
        """
        收集硬件信息，然后发送到服务器
        :return:
        """
        # 收集信息
        info = info_collection.InfoCollection()
        asset_data = info.collect()
        # 将数据打包到一个字典内，并转换为json格式
        data = {'asset_data': json.dumps(asset_data)}
        # 根据settings中的配置，构造url
        url = "http://%s:%s%s/" % (settings.Params['server'],
                                   settings.Params['port'],
                                   settings.Params['url'])
        print('正在将数据发送至：[%s] ……' % url)
        try:
            # 使用python内置的urllib.request库，发送post请求
            # 需要先将数据进行封装，并转换成bytes类型
            # data_encode = urllib.parse.urlencode(data).encode()
            # response = urllib.request.urlopen(url=url, data=data_encode,
            #                                   timeout=settings.Params['request_timeout'])  # 返回的时bytes
            # 使用requests模块发送请求
            response = requests.post(url=url, data=data, timeout=settings.Params['request_timeout'])

            print("\033[31m发送完毕！\033[0m")
            # message = response.read().decode()
            message = response.text
            print("返回结果：%s" % message)
        except Exception as e:
            message = "发送失败"
            print("\033[31m发送失败，%s\033[0m" % e)
        # 记录发送日志
        with open(settings.PATH, 'ab') as f:
            string = "发送时间：%s \t 服务器地址：%s \t 返回结果：%s \n" % (time.strftime('%Y-%m-%d %H:%M:%S'), url, message)
            f.write(string.encode('utf-8'))
            print("日志记录成功！")


if __name__ == '__main__':
    print('\033[31m你好,测试color\033[0m')
