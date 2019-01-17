from django.test import TestCase
from rest_framework.views import APIView
# Create your tests here.


from rest_framework import generics
from rest_framework import viewsets  # 可以传参

class GenericAPIView(views.APIView):
    def get_queryset(self):
        """获取序列化"""
        pass
    def get_serializer(self, *args, **kwargs):
        """获取序列化器"""
        pass


    def filter_queryset(self, queryset):
        """过滤条件"""
        pass