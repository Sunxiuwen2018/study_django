#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:SunXiuWen
# make_time:2018/11/7
from django.shortcuts import render, reverse, redirect
from django.http import JsonResponse
from django.views import View
from Rbac import models
from Crm.utils import md5  # 导入自定义的为密码进行加密的模块
from Rbac.service.init_permissions import init_permissions  # 导入自定义的权限初始化方法


class RegisterView(View):
    def get(self, request):
        """注册页面"""
        return render(request, './author/register.html')

    def post(self, request):
        """创建用户"""
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        # 给密码通过md5加密,md5不算是加密只是一种算法，且不可逆，一般通过“撞库”来解决
        password_md5 = md5.gen_md5(password)
        # 写入到数据库
        models.UserInfo.objects.create(username=username, password=password_md5, )
        # 用JsonResponse发送非dict数据，需要加safe参数
        return JsonResponse('{"code":3000, "mes":"注册成功"}', safe=False)


class LoginView(View):
    def get(self, request):
        """经过自定义中间件访问权限验证来到此处，给前端发送登陆页面
        """
        return render(request, "./author/login.html")

    def post(self, request):
        """
        经过中间件权限校验有访问权限后，来到此处，验证用户信息
        :param request:
        :return: 成功返回要访问的页面，及初始化访问权限信息
        """
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        # 因注册时将pwd经过md5加密了，所以校验时，需要把传过来的pwd进行md5，再和数据库校验
        user_obj = models.UserInfo.objects.filter(username=username, password=md5.gen_md5(password)).first()
        if not user_obj:
            return render(request, "./author/login.html", {"code": 4000, "mes": "用户名或密码错误"})
        # 用户验证通过，则为用户进行权限初始化
        """
        1、获取用户的权限        
        2、写入session
        """
        # 注意有的用户可能只是注册了，但没有分配权限，因此需要排除
        # 权限校验是很多地方都要用到的，故单独写一个函数
        init_permissions(user_obj, request)
        return redirect(reverse("crm:user_list"))  # 登录成功跳转到展示客户信息页面
