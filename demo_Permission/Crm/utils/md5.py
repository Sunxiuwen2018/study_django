#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:SunXiuWen
# make_time:2018/11/7
import hashlib


def gen_md5(pwd):
    """
    为密码进行md5加密
    :param pwd: 要加密的字符串
    :return:
    """
    obj = hashlib.md5("加盐".encode('utf-8'))  # 创建md5对象，并加盐
    obj.update(pwd.encode('utf-8'))  # 加密的数据必须是bytes
    return obj.hexdigest()
