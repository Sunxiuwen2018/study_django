#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:SunXiuWen
# make_time:2018/11/8
from django.conf.urls import url
from .views import authors
from .views import books

urlpatterns = [
    # 登录认证
    url(r'login/', authors.LoginView.as_view(), name="login"),
    # 查询全部和新增
    url(r'books/$', books.BookView.as_view(), name="books_list"),
    # 查询单个，更新，删除
    url(r'books/(\d+)/$', books.BookEditView.as_view(), name="book_change"),
]
