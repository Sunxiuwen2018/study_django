#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:SunXiuWen
# make_time:2018/11/7
"""
# from django.conf import global_settings
# from Permission import settings
创建了中间件，一定记得要注册
"""
import re
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings  # 更全,django内置很多setting文件
from django.http import HttpResponse
from django.shortcuts import (redirect,reverse)


class RbacMiddleware(MiddlewareMixin):
    """
    访问权限校验中间件
    """
    def process_request(self, request):
        """
        白名单校验,请求校验
        """
        # 请求经过wsgi后来到中间件，处理白名单，白名单应该是设置在setting中
        w_list = settings.VALID_LIST
        for w_url in w_list:
            if re.match(w_url, request.path_info):
                return None  # 通过白名单，无需做权限校验,继续执行后面的代码

        # 权限校验，去session中获取当前用户权限，然后对用户请求的url一一进行匹配
        permission_dict = request.session.get(settings.RBAC_PERMISSION_SESSION_KEY)
        print(permission_dict)
        """
        设置权限数据结构permission_dict={
        "url别名"：{"url":"/user/"}
        }
        """
        # 考虑第一次访问，后台还没有未其设置session
        # 因设置了白名单，登录是可以访问的，登录成功一定设置了session，如果
        # 没有，那么就一定是没有登录
        # 有个观念要清楚，登录后，跳转到对应的页面，是再次向后台发送了一次请求
        if not permission_dict:
            return redirect(reverse("crm:login"))

        for i in permission_dict.values():  # 获取字典的所有value
            # 注意路由匹配的先后，因此要为url加上开头和结尾匹配,如果，录入的时候没有加^$,就需要在这里加
            #  还有路劲前最重要的/也要加上
            url_ret = f"^{i['url']}$"
            if re.match(url_ret, request.path_info):
                return None
            # 如果所有的都没有匹配上
        return HttpResponse("无权访问,O(∩_∩)O")


# 另一思路
"""
        if not permission_dict:
            return redirect('/login/')

        flag = False
        for name, info in permission_dict.items():
            reg = "^%s$" % info['url']
            if re.match(reg, request.path_info):
                flag = True
                break
        if not flag:
            return HttpResponse('无权访问')

"""