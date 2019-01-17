#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:SunXiuWen
# make_time:2018/11/8
"""
基于token来认证用户
"""
from book_supermarket import models
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class MyAuthentications(BaseAuthentication):
    def authenticate(self, request):
        """认证必须定义的方法，用于校验用户带来的token
        Authenticate the request and return a two-tuple of (user, token).
        """
        # 获取token
        token = request.query_params.get("token", "")
        # 判断token
        if not token:
            # return Response({"code": 10002, "mes": "没有token"})
            raise AuthenticationFailed({"code": 10002, "mes": "没有token"})
        elif len(token) <= 32:
            raise AuthenticationFailed("长度不符合标准")
        # 校验token是否正确
        # 必须返回通过认证token后的user对象和token对象组成一个元组
        user_obj = models.User.objects.filter(token=token).first()
        print(user_obj)
        if not user_obj:
            raise AuthenticationFailed("无效的token")
        return user_obj, token
