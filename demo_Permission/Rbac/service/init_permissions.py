#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:SunXiuWen
# make_time:2018/11/10
"""用户用户的权限初始化"""
from django.conf import settings


def init_permissions(user_obj, request):
    """
    获取用户的访问权限列表，将权限封装到session中
    :param request:
    :return:
    """
    # 排除没有分配权限的人,角色查权限，多对多，反向查询
    permission_queryset = user_obj.role.filter(permission__id__isnull=False).values(
        "permission__id",
        "permission__title",
        "permission__name",
        "permission__url",
        "permission__menu__id",
        "permission__menu__title",
        "permission__menu__icon",
    ).distinct()
    """
     权限数据结构= {
            ‘url别名’：{‘url’:path}
        }
    """
    per_dict = {}
    for per in permission_queryset:
        key = per["permission__name"]
        value = {"url": per["permission__url"]}
        per_dict[key] = value

    """
    菜单数据结构= {
    一级菜单:{
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
}
    """
    menu_dict = {}
    # 一个菜单有多个子菜单即多个权限
    for menu in permission_queryset:
        # 没有菜单id的就不是菜单，应该排除掉
        menu_id = menu.get("permission__menu__id", "")
        if not menu_id:
            continue

        # 一个一级菜单下有多个子菜单，如果已经添加了一个一级菜单的
        # 子菜单，下次再次添加，就只需再添加子菜单即可
        if menu_id not in menu_dict:
            menu_dict[menu_id] = {
                "title": menu["permission__menu__title"],
                "icon": menu["permission__menu__icon"],
                "child": [
                    {
                        "title": menu["permission__title"],
                        "url": menu["permission__url"],
                    },
                ]
            }
        else:
            menu_dict[menu_id]['child'].append(
                {
                    "title": menu["permission__title"],
                    "url": menu["permission__url"],
                }
            )

    # 将权限封装到session中
    # 要定义好session的权限和菜单存放到字典中的key，在setting中定义好
    request.session[settings.RBAC_PERMISSION_SESSION_KEY] = per_dict
    request.session[settings.RBAC_MENU_SESSION_KEY] = menu_dict
