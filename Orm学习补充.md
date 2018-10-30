# 今日收获20181030:ORM

## 今日收获1：
>想创建不同版本的django的虚拟环境
    需要先创建虚拟环境，安装好指定版本，再用pycharm创建django项目，指定虚拟环境目录

>>步骤：
    1、pip3 install virtualenv
    2、cd 到目标目录
    3、virtualenv web   # 创建虚拟环境，生成web目录，web为环境名
    4、D:\Django>cd luffy_web\Scripts
    5、D:\Django\luffy_web\Scripts>activate.bat   激活虚拟环境
    (luffy_web) D:\Django\luffy_web\Scripts>
    (luffy_web) D:\Django\luffy_web\Scripts>deactivate.bat  退出虚拟环境
    6、pip3 install django==1.11.5
    7、django-admin startproject addmoney
    8、python manage.py startapp lu_demo
    9、通过pycharm打开项目，cmd进入虚拟环境

## 今日收获2：
>想把models中所有的类都在admin中注册，好在admin后台管理
    django：django123

>1、导入项目models文件
    from 项目名 import models

### 方式一：
>单个类在admin中注册：
    admin.site.register(models.Book)

### 方式二：
>批量导入
    1、在models.py中加入变量
    __all__ = ["Book", "Publisher", "Author"]
    2、在admin.py中，通过for循环__all__列表，注册
    for table in models.__all__:
        admin.site.register(getattr(models,table))

## 今日收获3：
    >每个类中加入meta类，显示中文表名
    class Meta:
        db_table = "xxx"   # 定义在数据库中的表名，默认是app+类名
        verbose_name_plural = db_table   # 定义在admin后天显示的表名，复数
    注：
    1、在类中字段中添加verbose_name="中文字段名" 可以在admin后天显示，且添加不用做数据迁移命令
    2、下面只能用于单个类注册，在后台显示表中的各个字段，在一个页面，choice字段会有问题
        class PermissionAdmin(admin.ModelAdmin):
            list_display = ['id','title', 'url','name' ]   # 类中的字段，展示
            list_editable = ['url', 'name']                # 其中的字段可以修改

# Django序列化解决方案
>需求：因为后端给前端都是json数据，因此需要将数据序列化，而orm数据类型都是queryset，故需要解决，方案如下

from django.http import HttpResponse, JsonResponse
from django.views import View  # 创建cbv必须继承的类
from lu_demo import models

class BookView(View):

    给前端数据展示
        book_list = [
            {
                id:1,
                title:"xx",
                pulisher:{title:xxx},
                authors:[{},{}]
            }
        ]


    def get(self, request):
        # 现状 queryset [<>,<>]
        # book_list = models.Book.objects.all()
        # <QuerySet [<Book: 8年工作纪实>, <Book: python速成记>, <Book: 人生苦短>]>
        # all()得到的是queryset列表,里面是对象，而传给前端必须是json格式，queryset无法转
        # Object of type 'QuerySet' is not JSON serializable

        # 方式一：通过values，得到queryset的字典[{},{}],通过list转换成列表!!!
        # 拿不到datetime类型
        """
        book_list = models.Book.objects.all().values("id", "title", )
        import json
        ret = json.dumps(list(book_list), ensure_ascii=False)  # 参数是将ascii码转码成中文
        return HttpResponse(ret)
        """
        # json无法序列化时间类型,set，能str,int,float，bool,list.tuple,dict,None

        # 方式二：django自带的JsonResponse，它可以序列时间，无法序列化外键关系
        # JsonResponse主要做了两件事
        # 1、继承HttpResponse
        # 2、做了序列换 =>json.dumps
        # 3、还序列化了datetime
        # HttpResponse  返回字符串
        # book_list = models.Book.objects.all().values("id", "title", "pub_time", "publisher")
        # 外键publisher拿到的是id
        # [{"id": 1, "title": "8年工作纪实", "pub_time": "2018-10-01", "publisher": 1},]
        # return JsonResponse(book_list)
        # In order to allow non-dict objects to be serialized set the safe parameter to False.
        # 为了允许非dict对象被序列化，将安全参数设置为False,需要设置参数sefe=False
        """
        return JsonResponse(list(book_list), safe=False,json_dumps_params={"ensure_ascii":False})
        # json_dumps_params 解决参数，显示中文
        """
        """
        # 想拿到的publisher的所有信息组成一个字典，故需要拿到对象然后询环publisher：{title：xx，name：xx}
        book_list = list(book_list)
        for book in book_list:
            publisher_obj = models.Publisher.objects.filter(id=book["publisher"]).first()
            book["publisher"] = {
                "id": publisher_obj.id,
                "title": publisher_obj.title
            }
        return JsonResponse(book_list, safe=False, json_dumps_params={"ensure_ascii": False})

        # 含有chioce字段，默认拿到的是id，希望拿到的是值，且是需要对象才能拿到obj.get_字段名_display()
        # manytomany字段也和外键一样需要循环
        # 上面的解决都非常的复杂，django提供了终极的方法
        """
        # 方式三：django带的能够解决queryset序列化
        # 优点：可以序列化queryset，但外键关系依然不能序列化，取出来的还是id
        """
                [
              {
                "model": "lu_demo.book",
                "pk": 1,
                "fields": {
                  "title": "8年工作纪实",
                  "category": 3,
                  "pub_time": "2018-10-01",
                  "publisher": 1,
                  "authors": [
                    1
                  ]
                },
              },]
        """
        from django.core import serializers
        book_list = models.Book.objects.all()
        ret = serializers.serialize("json", book_list, ensure_ascii=False)
        return HttpResponse(ret)

