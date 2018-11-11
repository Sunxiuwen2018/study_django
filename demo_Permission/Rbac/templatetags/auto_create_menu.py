#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:SunXiuWen
# make_time:2018/11/10
"""用于自动生成菜单标签"""
from django import template
from django.conf import settings

register = template.Library()


@register.inclusion_tag("auto_create_menu.html")
def create_menu(request):
    """获取session中的菜单字典，html中就可以使用了
        菜单数据结构= {
    一级菜单id:{
        一级菜单名：
        一级菜单的图标：
        二级菜单: [
            {
                二级菜单1的title：
                二级菜单1的url：
            }，
            {
                二级菜单1的title：
                二级菜单1的url：
            }
        ]
    }

    :param request:
    :return: 返回菜单字典
    """
    menu_dict = request.session.get(settings.RBAC_MENU_SESSION_KEY)
    return {"menu_dict": menu_dict}


@register.filter
def check_btn(btn_url, request):
    """
    用于判断是否生成按钮，返回值为bool
    权限数据结构= {
            ‘url别名’：{‘url’:path}
        }
    :param btn_url: 按钮的url别名
    :param request: request请求对象
    :return: True or False
    """
    per_dict = request.session.get(settings.RBAC_PERMISSION_SESSION_KEY, "")
    if btn_url in per_dict:
        return True
    else:
        return False
