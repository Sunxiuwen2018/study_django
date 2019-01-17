#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:SunXiuWen
# make_time:2018/11/8
"""
书籍的增删改查

总结：
使用序列化操作步骤：
1、创建序列化器，根据model字段建立，正反序需要显示的字段及内容
2、创建url，使用序列化必须用cbv，
3、创建视图cbv，获取对象queryset，应用序列化器
4、返回序列化后的数据

通过本次实验可以得出序列化器一共有三种传参
1、BookSerializer(queryset, many=True)   直接传queryset，就是序列化，many只是允许多个值序列化
2、BookSerializer(data=request.data)    这是反序列化
3、BookSerializer(instance=queryset_obj, data=request.data, partial=True)  这是部分更新，告诉谁要更新，数据是，可以部分更新
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from book_supermarket import models
from book_supermarket.utils.my_serializers import BookSerializer
from book_supermarket.utils.my_authentions import MyAuthentications

class BookView(APIView):
    # authentication_classes = [MyAuthentications,]

    def get(self, request):
        """获取所有"""
        queryset = models.Book.objects.all().select_related()
        ser_obj = BookSerializer(queryset, many=True)  # 允许序列化多个
        return Response(ser_obj.data)

    def post(self, request):
        """增加数据:反序列化"""
        # 前端发过来的数据都会封装在重新封装的request对象的data中
        obj = request.data
        # 进行反序列化
        ser_obj = BookSerializer(data=obj)
        print(ser_obj)
        # 进行数据校验
        if not ser_obj.is_valid():
            # 没有通过，则返回报错
            return Response({"code": 1000, "error_mes": ser_obj.errors})
        # 验证通过则保存到数据库
        ser_obj.save()
        # 验证通过的数据都保存在validated_data中
        return Response(ser_obj.validated_data)


class BookEditView(APIView):
    def get(self, request, id):
        """获取部分,多了个id参数"""
        print(id)
        queryset = models.Book.objects.filter(id=id).first()
        if not queryset:
            return Response({"code": 1000, "error": "无效的数据"})
        ser_obj = BookSerializer(queryset)
        return Response(ser_obj.data)

    def patch(self, request, id):
        """部分更新"""
        # 获取对象c
        queryset_obj = models.Book.objects.filter(id=id).first()
        # 反序列化
        ser_obj = BookSerializer(instance=queryset_obj, data=request.data, partial=True)  # partial 允许部分跟新
        # 校验
        if not ser_obj.is_valid():
            return Response({"code": 1000, "error_mes": ser_obj.errors})
        # 校验完毕后记得保存
        ser_obj.save()
        return Response(ser_obj.validated_data)

    def delete(self, request, id):
        """删除"""
        queryset_obj = models.Book.objects.filter(id=id).first()
        if not queryset_obj:
            return Response({"code": 1001, "error": "删除的数据不存在"})
        queryset_obj.delete()
        return Response({"code": 2000, "msg": "删除成功"})

