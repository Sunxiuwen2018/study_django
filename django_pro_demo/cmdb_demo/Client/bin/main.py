#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:SunXiuWen
# make_time:2019/1/15
import os
import sys

# 获取当前工作目录的根目录
BASE_DIR = os.path.dirname(os.getcwd())

# 设置工作目录，使得包和模块能够正常导入
sys.path.append(BASE_DIR)

from core import handler

if __name__ == '__main__':
    handler.ArgvHandler(sys.argv)
