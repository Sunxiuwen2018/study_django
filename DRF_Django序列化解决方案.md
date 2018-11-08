# Django序列化解决方案
**Serializer 序列化后的数据放在data方法里**
>需求：因为后端给前端都是json数据，因此需要将数据序列化，而orm数据类型都是queryset，
 故需要解决，方案如下

>views.py
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

# Django终极解决序列化武器：DRF框架
>专门解决后端数据序列化Api接口
    1、用CBV方式创建视图，继承APIView
    2、django中返回值用HttpResponse、JsonResponse、render、DRF用Response

## 使用DRF
>   1、下载djangorestframework
        pip3 install djangorestframework
    2、在django中setting里注册app
        "rest_framework"

    3、 声明一个序列化器，前后端交互需要的字段、在项目目录下创建一个my_serializers.py文件
         from rest_framework import serializers
         from lu_demo import models

        class PublisherSerializer(serializers.Serializer):
            id = serializers.IntegerField()
            title = serializers.CharField(max_length=32)

        class AuthorSerializer(serializers.Serializer):
            id = serializers.IntegerField()
            name = serializers.CharField(max_length=32)

        class BookSerializer(serializers.Serializer):
            """字段要与models一一对应，没有就不校验"""
            id = serializers.IntegerField(required=False)
            title = serializers.CharField(max_length=32)

            Choices = ((1, "python"), (2, "linux"), (3, 'go'))
            category = serializers.CharField(max_length=32, source="get_category_display", read_only=True)  # get
            pub_category = serializers.ChoiceField(choices=Choices, write_only=True)  # post

            pub_time = serializers.DateField()

            publisher = PublisherSerializer(read_only=True)
            publisher_id = serializers.IntegerField(write_only=True)
            # 嵌套的序列化
            authors = AuthorSerializer(many=True, read_only=True)
            author_list = serializers.ListField(write_only=True)

            def create(self, validated_data):
                # 执行orm的新增数据的操作
                book_obj = models.Book.objects.create(title=validated_data["title"],
                                                      category=validated_data["pub_category"],
                                                      pub_time=validated_data["pub_time"],
                                                      publisher_id=validated_data["publisher_id"])
                # 更新多对多字段
                # book_obj.authors.add(*validated_data["author_list"])  # add 是增加对象，set是整加列表
                book_obj.authors.set(validated_data["author_list"])
                print(validated_data["author_list"])
                return book_obj

            def update(self, instance, validated_data):
                # 有就更新没有就取默认的
                instance.title = validated_data.get("title", instance.title)
                instance.category = validated_data.get("pub_category", instance.category)
                instance.pub_time = validated_data.get("pub_time", instance.pub_time)
                if validated_data.get("author_list"):  # 判断有没有多对多字段
                    print(validated_data["author_list"])
                    instance.authors.set(validated_data["author_list"])
                instance.save()
                return instance

        4、在view.py中导入
            from rest_framework.views import APIView      # 要继承的类
            from rest_framework.response import Response  # 返回函数
            from .my_serializers import BookSerializer    # 导入自定义声明的序列化器

        class BookViewDRF(APIView):
            def get(self, request):
                # 查看所有的数据
                book_list = models.Book.objects.all()
                # many 表示多个字段
                # 声明序列化器，是像models一样创建一张表
                ser_obj = BookSerializer(book_list, many=True)
                return Response(ser_obj.data)

            # 反序列化
            def post(self, request):
                book_obj = request.data
                print(book_obj)
                ser_obj = BookSerializer(data=book_obj)
                if ser_obj.is_valid():
                    print(ser_obj.validated_data)
                    ser_obj.save()  # 必须重写create方法,保存到数据库
                    return Response(ser_obj.validated_data)
                else:
                    return Response(ser_obj.errors)

        class BookEditView(APIView):
            def get(self, request, id):
                """查看单条数据"""
                book_obj = models.Book.objects.filter(id=id).first()
                ser_obj = BookSerializer(book_obj)
                return Response(ser_obj.data)

            # def put(self,requst,id):pass  # 更新全部

            def patch(self, request, id):  # 单个更新
                book_obj = models.Book.objects.filter(id=id).first()
                # partial=True  允许部分验证，就可以改单个字段了
                ser_obj = BookSerializer(instance=book_obj, data=request.data, partial=True)
                if ser_obj.is_valid():
                    ser_obj.save()
                    return Response(ser_obj.validated_data)
                else:
                    return Response(ser_obj.errors)

        5、urls.py
            from django.conf.urls import url
            from lu_demo import views

            urlpatterns = [
                url("test/", views.test, name='test'),
                url("books/", views.BookView.as_view(), name='book'),
                url("api/book/$", views.BookViewDRF.as_view()),
                url("api/book/(?P<id>\d+)", views.BookEditView.as_view()),


