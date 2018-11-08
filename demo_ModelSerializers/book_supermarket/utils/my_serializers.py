#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:SunXiuWen
# make_time:2018/11/8
from rest_framework import serializers
from book_supermarket import models


class BookSerializer(serializers.ModelSerializer):
    # 下面这种直接指定model字段可以拿到choice后的文字，但有一个确定，当反序时，前端给的是id，这里却是文字，验证会报错
    # category = serializers.CharField(source="get_category_display", )
    """默认choice、fk，多对多，返给前端的都是id，所以需要定义
    让其显示文字，但当前端传过来的只是id或部分，这是就又可以用id来显示了
    通过定义read_only,write_only 来让字段正/反序是否显示，rquierd 反序也是不显示的
    """
    category_dis = serializers.SerializerMethodField(read_only=True)
    publisher_info = serializers.SerializerMethodField(read_only=True)
    authors_info = serializers.SerializerMethodField(read_only=True)

    def get_category_dis(self, obj):
        """get_字段名
            choice字段
            obj为操作对象,如book对象
        """
        return obj.get_category_display()

    def get_publisher_info(self, obj):
        """fk"""
        return {"id": obj.publisher.id, "title": obj.publisher.title}

    def get_authors_info(self, obj):
        """多对多"""
        # ret = []
        # author_list = obj.author.all().select_related()
        # for author in author_list:
        #     id = author.id
        #     username = author.username
        #     ret.append({"id": id, "username": username})
        # return ret
        return [{"id": author.id, "username": author.username} for author in obj.author.all()]

    class Meta:
        model = models.Book
        fields = "__all__"
        # 想要将自定义的额外字段显示出来需要用下面,并且定义某些字段在正序或反序中是否显示,或者某些字段进行处理
        # 写ready_only 为false，无效
        extra_kwargs = {
            # 定义了自定义显示的字段，那么对应的model字段就需要让他不要显示，而反序是不需要返回文字的就可以显示
            "category": {"write_only": True},
            "publisher": {"write_only": True},
            "author": {"write_only": True},
        }



