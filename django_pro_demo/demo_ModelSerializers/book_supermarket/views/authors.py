#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:SunXiuWen
# make_time:2018/11/8
"""
用于用户校验认证方面views

流程：
1.创建自己的认证器
2.应用认证器
3.创建token或session
4.返回状态，实际中跳转页面
"""
import uuid
from book_supermarket import models
from rest_framework.views import APIView
from rest_framework.response import Response


class LoginView(APIView):
    # 走到这里来了，是已经做过认证了，现在只需要验证账户信息
    def post(self, request):
        # print(request.auth)
        # 获取用户账户密码[前后端协商好用户名和密码用的参数名]
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        # 校验
        user_obj = models.User.objects.filter(username=username, password=password).first()
        if not user_obj:
            return Response({"code": 1500, "mes": "用户名或密码错误"})
        # 登录成功，为用户创建一个token,然后写入到数据库
        token = uuid.uuid4()
        user_obj.token = token
        user_obj.save()
        return Response({"code": 20001, "mes": "login successful", "token": token})
