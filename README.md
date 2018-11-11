# 第一部分：Django回顾
## 简叙http协议？
```
    Http协议全称为超文本传输协议，是基于tcp/ip协议进行通信的，它的显著特点是无状态，短连接，主要表现为服务端处理一次请求就会断开连接，且不保存用户状态，也就是说，客户端请求响应后，再次发送请求时，服务端还是不认识客户端，解决的方式之一就是建立session在服务端保存状态。再就是http的请求报文格式和响应报文格式主要都分为两部分请求头和请求体，响应头和响应体，请求头与请求头，响应头与响应头之间通过\r\n分割，请求头与请求体，响应头与响应体之间通过2个\r\n分割。
    再就是常见的get请求是没有请求体的，它的数据是拼接在url上的，而post请求是放在请求体中的。
```
## 你了解的请求头都有哪些？
1. ACCEPT: 告诉服务端浏览器能够解析的数据格式
2. User-Agent： 告诉服务器客户端的设备信息，如是什么浏览器，系统版本等等
3. referer： 存放来源地址告诉服务器是从那里来的，可以用作防盗链
4. host: 当前访问的主机名称
5. Conten-type：请求提交的数据格式，一般用于post/put/patch请求
6. Cookie： 将cookie信息带给服务器

## 你了解的响应头有哪些？
1. Conten-type：告知浏览器响应的数据格式
2. Server：告知浏览器，服务器的类型，如nginx等等
3. Location: 告知浏览器找谁，一般重定向，会在这里显示要去的url，redirect的本质就是在响应中加了一个Location响应头
4. set-cookie: 服务器返回的cookie
5. connection：服务端设置响应后，是否断开连接 close/keep-alive

## 你所了解的请求方式有哪些？
1. GET/HEAD/POST/PUT/PATCH/DELETE/OPTIONS
2. OPTIONS在解决跨域问题时有用，先发送预检
3. put是全部更新，patch是局部更新

## Django请求的生命周期？
1. 先将输入url发送给dns服务器进行域名解析，获得ip地址；
2. 浏览器根据获得的ip和端口号（默认80）创建连接（tcp/ip三次握手），发送请求；
3. 服务端接收到请求，具体为实现了wsgi协议的模块，如wsgiref或uwsgi接收到用户请求；
4. 然后将其转发给中间件，执行各个中间件的process_reqeust，process_view等方法；
5. 然后路由系统进行路由匹配，匹配成功则执行对应的视图函数；
6. 视图函数进行业务处理（如通过orm操作数据库，模板的渲染）；
7. 然后视图将处理的结果交给中间件的process_response方法处理；
8. 中间件处理完后，通过wsgiref等模板将结果返回给浏览器。
9. 然后断开连接。（四次挥手）
10. 浏览器获得数据进行渲染，然后断开连接。

>注：默认渲染的本质是将模板中特殊的标签，进行字符串的替换
必须会画django请求生命周期图

## 浏览器上输入`http://www.baidu.com`地址回车发生了什么？【问题本质同上面一样】
1. 先将输入url发送给dns服务器进行域名解析，获得ip地址；
2. 浏览器根据得到的ip和端口号，创建连接，发送请求。
3. 服务端接收到请求，根据http协议解析请求，获取url，执行对应的业务函数
4. 然后将处理后的资源（html代码的字符串）返回给浏览器
5. 浏览器接收到响应，然后将资源进行渲染展示，最后断开连接。

## 什么是wsgi？
1. wsgi全称为web服务网关接口，是一套协议，主要是定义了客户端与服务端通信的一种规范，它的本质是实现socket的服务端。实现这个协议的常用模块主要有wsgiref（测试），uwsgi（生产）。

## 自己实现web框架？
1. 本质：创建一个socket服务端，先发送一个响应头包含http协议，状态码，状态描述符ok
```
    import socket
    connect = socket.socket()
    connect.bind(('127.0.0.1',80))
    connect.listen()
    while True:
        conn,addr = connect.accept()
        conn.recv(1024)
        conn.send("HTTP/1.1 200 OK \r\n\r\n")
        conn.send(b'hello world')
```

## wsgi实现原理？
```
    from wsgiref.simple_server import make_server

    class WSGIHandler(object):
        def __call__(self,environ, start_response):
            """
            一旦请求到来会执行此方法,面向对象，一旦实例化就会调用__call__方法
            :param environ: 请求相关的所有数据
            :param start_response: 响应头相关数据
            :return:
            """
            start_response('200 OK', [('Content-Type', 'text/html')])
            return [bytes('<h1>Hello, web!</h1>', encoding='utf-8'), ]

    obj = WSGIHandler()

    if __name__ == '__main__':
        httpd = make_server('127.0.0.1', 8000, obj)
        httpd.serve_forever()
```

## django中间件的作用？应用场景？
1. 中间件，是django处理请求和响应的框架级别的钩子，可以对所有的请求和响应进行批量操作，在执行视图函数前后做一些额外的操作

2. 应用场景：
    - 【内部玩】
        * 记录日志 （在process_request方法中用logging模块，待添加实现代码）
        * IP黑白名单（待添加实现代码）
    - 权限系统中的权限校验

    - 登录

    - 解决跨域：编写一个中间件，在中间件中定义一个process_response方法，添加一个响应头（CORS,跨站资源共享）
    ```
        from django.utils.deprecation import MiddlewareMixin

        class MyCors(MiddlewareMixin):
            def process_response(self, request, response):
                # 简单请求
                response["Access-Control-Allow-Origin"] = "*"
                # 复杂请求 会先发送预检请求 OPTIONS
                if request.method == "OPTIONS":
                    response["Access-Control-Allow-Headers"] = "Content-Type"
                    response["Access-Control-Allow-Methods"] = "POST, PUT, PATCH, DELETE"
                return response
    ```

    - 跨域的原因：浏览器同源策略导致，只要访问的域名或端口和请求方任一个不一致就会造成跨域现象
    浏览器其实拿到了数据，但因同源策略进行了拦截

    - csrf_token验证（django内置功能）
    - 原因，解决方法???
    - rest_formawork视图类继承APIVIEW,而APIVIEW,重写了as_view方法，返回值进行了csrf_token豁免了view方法

3. 中间件主要有5个方法

    > process_request(self,request)
    - 按顺序执行，有返回值时，django版本1.10以后 ==>平级返回;
    - django版本1.10以前 ==> 找到最后一个中间件的process_reponse开始返回，不会走视图函数

    > process_view(self,view_func,view_args,view_kwargs)
    - 先走路由系统获取视图的函数名，和参数，有返回值，直接执行最后一个中间件的process_response方法
    - 这时不走视图函数

    - process_template_response(self,request,response)
    - process_exception(self,request,exception)
    - process_response(self,request,response)

## Django中间件执行顺序的流程源码实现原理
>代码模拟
    ```
    """
    1、将每个类添加一个列表中，循环列表进行实例化，然后调用类中的方法，将方法名添加到配置好的方法列表中，
    2、循环每个存放方法名的列表，依次按顺序执行，就达到了中间件5个方法的执行顺序了
    """
        class M1(object):
            def process_request(self, request):
                print("M1_process_request")

            def process_view(self, request, view_func, *args, **kwargs):
                print("M1_process_view")

            def process_exception(self, request, exception):
                print("M1_process_exception")

            def process_template_response(self, request, response):
                print("M1_process_template")

            def process_response(self, request, response):
                print("M1_process_response")


        class M2(object):
            def process_request(self, request):
                print("M2_process_request")

            def process_view(self, request, view_func, *args, **kwargs):
                print("M2_process_view")

            def process_exception(self, request, exception):
                print("M2_process_exception")

            def process_template_response(self, request, response):
                print("M2_process_template")

            def process_response(self, request, response):
                print("M2_process_response")


        class M3(object):
            def process_request(self, request):
                print("M3_process_request")

            def process_view(self, request, view_func, *args, **kwargs):
                print("M3_process_view")

            def process_exception(self, request, exception):
                print("M3_process_exception")

            def process_template_response(self, request, response):
                print("M3_template_response")

            def process_response(self, request, response):
                print("M3_process_response")


        # 将类放入到一个列表中
        middleware = [M1, M2, M3]

        # 创建存放5种方法的列表
        process_request_list = []
        process_view_list = []
        process_response_list = []
        process_exception_list = []
        process_template_response_list = []

        # for循环，进行每个类的实例化，并将每个方法名加入到对应[方法名]的列表
        for m in middleware:
            obj = m()  # 知识点：面向对象一旦实例化就会执行类中的__call__方法
            process_request_list.append(obj.process_request)
            process_view_list.append(obj.process_view)
            process_response_list.insert(0, obj.process_response)
            process_exception_list.append(obj.process_exception)
            process_template_response_list.append(obj.process_template_response)  # 因为response是倒序执行的

        # for循环执行对应的方法，就能按各自注册顺序执行对应方法了
        for func in process_request_list:
            func("request")
        for func in process_view_list:
            func("request", "view_func")
        for func in process_response_list:
            func("request", "response")
    ```

## 根据类的路劲找到类并实例化【根据反射找到模块中的成员】  反射是亮点，可以说反射在这里用到
>代码模拟
    import importlib

    path = "handler.basic.BaseHandler"
    func_name = "process_request"

    - 根据字符串的形式导入模块
      module_path, cls_name = path.rsplit('.', maxsplit=1)

      module = importlib.import_module(module_path)  # 等同于 import handler.basic 导入模块的路径

    - 去模块中找到 BaseHandler 的类
      cls = getattr(module, cls_name)

    - 根据类() 实例化。
      obj = cls()

    - 执行对象.process_request方法
      func = getattr(obj, func_name)
      func()

## 路由系统 Urls

    >url与视图函数的映射表urlpatternts的配置：

        >> 由一个列表组成，url(正则表达式，视图函数，参数，别名)
        url(r'^api/$', views.test, {"params":"yyy"}, name="xxx")  ==> def test(request, args, params="xxx", kwargs):pass

    >url的无名分组和命名分组

        >> 无名分组：将url中匹配的的值，以位置参数传给视图函数 url(r'api/([1-9][0-9]{3})/$', views.test , name= "test")

                def test(request, '2018'):pass

        >> 命名分组：将url中匹配的值，以关键字得形式传给视图函数 url(r'api/(?p<year>[1-9][0-9]{3}/$)'，views.test,name="test")

                def test(request, yerar='2018'):pass

    >url的命名和反向解析，为每个url添加name属性，设置一个别名name="xxx"，在视图和模板中需要填写url时就可以通过name设置的别名进行反向解析，方便需要变更url时统一修改

        >> 在视图中应用：from django.shortcuts import reverse
                    无名：  return redirect(reverse("xxx"， args=(2018,)))
                    命名：  return redirect(reverse("xxx", kwargs={"year": 2018}))
        >> 在模板中应用：
                    无名： {% url "xxx" '2018'%}
                    命名： {% url "xxx" year='2018' %}

    >url命名空间，实现url分发，避免多个app中url别名相同报错，通过include()参数为每个app设置namespace别名

        from django.conf.url import include

        url(r"app01/", include("app01.urls", namespace="app01"))

        >>在视图中应用：
            redirect(reverse('app01:xxx', args=(2018,)))
            redirect(reverse('app01:xxx', kwargs={"year":2018}))

        >>在模板中应用：
            {% url "app01:xxx" '2018' %}
            {% url "app01:xxx" year='2018' %}

    - 扩展：可以这样添加url到列表中,同DRF中的路由封装
        urlpatterns += [
            url(r'^index/$', views.index),
        ]

    - 扩展路由分发的另一个方法，也体现include的本质，返回3元组
      urlpatterns = [
            url(r'^admin/', admin.site.urls),
            url(r'^index/', views.index,name='index'),
            url(r'^user/edit/(\d+)/$', views.user_edit,name='user_edit'),
            url(r'^crm/', include('app01.urls',namespace='crm')),
            url(r'^crm/', ([
                                url(r'^c1/', views.index),
                                url(r'^c2/', ([
                                                    url(r'^c3/', views.index,name='c3'), # 反向：reverse（‘n1:n2:c3’）
                                                    url(r'^c4/', views.index),
                                              ],None,'n2')),
                           ],None,'n1')),
        ]

## 视图系统 View
1. 软件架构模式
    - MVC model view controller
    - MTV  modele template view
    - M 操作数据库
    - V 执行业务逻辑
    - C 控制器

    ```
    Django的软件架构模型(MTV)     通用模型(MVC)
        M(model)            --->    M(model)
        T(template)         --->    V(view)
        V(view,urls)        --->    C(controller)
    ```

2. FBV和CBV的本质区别和联系？

    >**区别**
    - FBV 是以函数的形式处理业务逻辑
    - CBV 是以类的形式处理业务逻辑

    >**本质**
    - FBV和CBV都是都是一样的，因为url对应的都是一个函数
    1.FBV是一旦请求过来，就直接对应的视图函数；
    2.CBV是请求过来先执行视图类的as_view()方法，返回view函数，而view方法又会触发dispatch方法，dispatch方法会根据method不同，通过反射执行类中定义对应的请求方法；

3. 视图函数的返回值？
    - **主要有三种HttpResponse、render、redirect**
    - 本质都是继承HttpReponse，向浏览器返回一个字符串
    - HttpResponse 直接返回一个字符串
    - render 通过模板渲染（读取html模板和数据，将模板中的特殊标记替换成数据)之后以字符串的形式返回
    - redirect 本质是将要重定向的地址添加到响应头Location中返回给浏览器

> 两个用于理解模板渲染的示例
```
    示例1：
        视图：
            def test(request):
                """
                :param request:
                :return:
                """
                return render(request,'test.html',{'k1':‘python’})
        test.html
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="x-ua-compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <title>Title</title>
            </head>
            <body>
            <div>
                <h1>{{ k1 }}</h1>
                <script>
                    alert('{{ k1 }}'); --->alert('python')--->打印出
                </script>
                <script>
                    alert({{ k1 }}); ---> alert(python) --->报错
                </script>
            </div>
            </body>
            </html>
    示例2：
        视图：
        test.html
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="x-ua-compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <title>Title</title>
            </head>
            <body>
            <div>
                <h1>{{ k1 }}</h1>
                <script src='/static/commons.js'></script>
            </div>
            </body>
            </html>

        commons.js
            alert('{{k1}}')  ---> 会alert出一个`{{k1}}`
```
4. 扩展：两个系统之间进行相互数据传输，A向B发送post请求，但B没有获取到数据，可能原因是？
    * 确认网络是否相通，查看日志是否有请求过来
    * 如有接到请求，可能是csrf拦截了，没有数据，需要进行csrf豁免，为视图加装饰器
    * 通过request.body查看请求体，request.POST解析时是有限制的，因为reqeust.POST是将请求体的数据转换成QueryDict对象；
    * 而request.POST 将原生的请求体转成QueryDict对象，请求必须满足两个条件才能转换：
     1、 Conten-Type：application/x-www-form-urlencoded
     2、 数据格式： key=value&key=value的形式
    如不满足此条件，django请求体就需要自行从reqeust.body获取值，并反序列化

    >**总结：**
    >> - django获取请求体，通过request.body
       - request.POST是将请求体的数据转换成了QueryDict对象

>**代码演练**
```
    1. csrf_token
            from django.views.decorators.csrf import csrf_exempt,csrf_protect

            @csrf_exempt
            def api(request):
                """
                为李超提供的API接口
                :param request:
                :return:
                """
                print(request.POST)
                return HttpResponse('...')


            实例代码：
                李超.py：
                    import requests
                    response = requests.post('http://127.0.0.1:8000/crm/api/',data={'user':'alex','pwd':'dsb'})
                    print(response.text)

                    Http请求格式：
                        """POST /crm/api/ http\1.1\r\nhost:..\r\nContent-Type:application/x-www-form-urlencoded .....\r\n\r\nuser=alex&pwd=dsb"""


                django服务端：

                    from django.views.decorators.csrf import csrf_exempt,csrf_protect

                    @csrf_exempt
                    def api(request):
                        """
                        为李超提供的API接口
                        :param request:
                        :return:
                        """
                        print(request.POST)
                        return HttpResponse('...')
    2. request.POST解析时，有限制。

            李超.py

                import requests
                response = requests.post('http://127.0.0.1:8000/crm/api/',json={'user':'alex','pwd':'dsb'})
                print(response.text)

                Http请求格式：
                    """POST /crm/api/ http\1.1\r\nhost:..\r\nContent-Type:application/json .....\r\n\r\n{'user':'alex','pwd':'dsb'}"""

            django服务端：
                @csrf_exempt
                def api(request):
                    """
                    为李超提供的API接口
                    :param request:
                    :return:
                    """
                    print(request.body) # 原生的请求体格式，有数据；（自己读取body然后进行解析）
                    print(request.POST) # 将原生的请求体转换成 QueryDict对象，无数据。
                    return HttpResponse('...')
```

## 模板系统 Template
> 将分发进行到底，可以将在自己的app中建立template、urls、views
1. 模板的查找顺序
    - 先去根目录下的templates文件夹中寻找
    - 根据app的注册顺序，去每个app的templates文件夹中寻找，只要有相同命名的模板就按顺序获取渲染（已验证）

2. 模板的继承
    **母版**
    - 定义bash.html 放在templates中（可创建归类目录，引用时加上目录path即可）
    - 模板中应用：{% extends 'bash.html' %}
    - 注意：且必须写在文件第一行，不然报错

    **代码块block**
    - 在母版中定义block留白，{% block block_name %}...{% endblock %}
    - 在模板中应用：{% block block_name %}变更的内容{% endblock %}
    - 注意：如不引用block，原母版中此处是什么，就显示什么，一旦引入就会更新，没有内容，该区域就为空白

    **组件include**
    - 单独写一段html标签，保存一个文件nav.html，如常见的导航条
    - 在模板中应用：{% include 'nav.html' %}
    - 注意：如果模板中存在继承和include，那么模板引擎会将所有的模板拼接到一起后再进行渲染(字符串替换)

    **静态文件static**
    - 常见的link标签，或img引入静态文件路劲，不写硬路劲
    - 在模板中应用：先在文件引入母版后面引入{% load static %}，后在对应位置写对应路径如src= '{% static "css/main.css" %}'

3. 模板语法和标签

    **模板获取索引，得到对应得value显示**
    - 列表： field.0     field = []
    - 字典： field.key   field = {}

    **模板中传递方法**
    - 视图返回方法名：render(request, 'index.html', {'func_name':func})
    - 模板中应用：{{ func }}
    - 注意：模板中引入方法，是无法传参数的

    **过滤器**
    - 使用方法{{变量|fileter:args}}
    - 常见过滤器：支持链式操作
        * default  设置默认值，如表格中某个单元格没有值设置一个默认值
        * length   返回变量的长度
        * filesizeformat   返回文件大小让人可读，kb,mb
        * date:"Y-m-d H:i:s"    返回格式化的时间格式2016-11-01 18：08：08
        * safe      在一串标签代码使用，表示受信任的，浏览器就不会解析成字符串
        * add
        * upper/lower/title
        * join  列表拼接成字符串  value= ["china","big"] {value|join}

    **自定义函数filter、simple_tag、inclusion_tag**
    - 模板中引入的方式都相同 {% load filename.py %}
    - 都可以在视图中通过name定义别名，一旦定义了别名，就不能用函数名
    - filter只能最多传两个参数，simple_tag可以传多个
    - inclusion_tag 返回一小段html代码
    - simple_tag一般用于给页面返回一个结果
    - filter也是返回一个结果，但可以作为if后面的条件，simple_tag不行
        * 在app或项目下建立一个目录名必须是`templatetag`的目录,在其目录创建一个py文件
        * 引入模块template：  from django import template
        * 创建一个变量名必须是`register`：register= template.Library()
    - 自定义filter
        - 函数：
        ```
            @rigester.filter
            def add_china(value,args):
                """一般用于对变量进行修饰，返回一个结果"""
                return "{}_{}".format(value,args)
        ```
        - 模板中应用：
        ```
            {{"big"|add_china:"@"}}
            {% if "xxx"|add_china:"yyy" %}<h1>love</h1>{% endif %}
        ```
    - 自定义simple_tag
        - 函数：
        ```
            @rigester.simple_tag
            def func(x,y,z):
                """一般用于给页面返回一个结果"""
                return x + y + z
        ```
        - 模板中应用：
        ```
            {% func "good" "good" "study"  %}
        ```
    - 自定义inclusion_tag
        - 函数：
        ```
            @rigister.inclusion_tag('tag.html')
            def fun1(x,y)
                """将传入的值在tag.html中应用，再返回代码块"""
                return {"x":x,"y":y}
        ```
        - 模板中应用：
        ```
            {%  func1 "dog" "bug" %}
        ```

## 模型系统
1. ORM 关系对应映射
    - 类     ---> 表
    - 对象   ---> 行
    - 属性   ---> 字段

2. 创建model类
    - 导入 from django.db import models
    - 创建类，继承modle.Modle
    ```
        class Goods(models.Model):
            title = models.CharField(verbose_name="商品名称", max_length=32)
            price = models.IntegerField(verbose_name="价格")
            source = models.ForeignKey(verbose_name="供货商", to="Source",on_delete=models.CASCADE)
            category_choices = (
                (1, "生活用品"),
                (2, "计生用品"),
                (1, "食品"),
                (1, "生鲜"),
            )
            category = models.CharField(verbose_name="种类", choices=category_choices, max_length=32)
            store_room = models.ManyToManyField(verbose_name="仓库", to="StoreRoom")
            purchase_date = models.DateTimeField(verbose_name="进货日期")
    ```
    - FK 一对多
        - 子表从母表中选出一条数据一一对应，但母表的这条数据还可以被其他子表数据选择、共同点是在admin中添加数据的话，都会出现一个select选框，但只能单选，因为不论一对一还是一对多，自己都是“一”
        * on_delete:
            ```
                models.CASCADE，删除供货商，则将改供货商下的厂商全部删除。 + 代码判断
                models.DO_NOTHING，删除供货商，引发错误IntegrityError
                models.PROTECT，删除供货商，引发错误ProtectedError
                models.SET_NULL，删除供货商，则将改供货商下的厂商所属供货商ID设置为空。（将FK字段设置为null=True）
                models.SET_DEFAULT，删除供货商，则将改供货商下的厂商所属供货商ID设置默认值。（将FK字段设置为default=2）
                models.SET，删除供货商，则将执行set对应的函数，函数的返回值就是要给改供货商下厂商设置的新的供货商ID。
                    例如：
                        def func():
                            models.Users.......
                            return 10

                        class MyModel(models.Model):
                            user = models.ForeignKey(to="User",to_field="id"on_delete=models.SET(func),)

                方法：
                    models.CASCADE， 删除逻辑时，通过代码判断当前 “供货商” 下是否有用户。
                    models.SET_NULL，稳妥。
                    沟通之后在确定。
            ```
        * db_constraint:
            - 待补充？？？？？
            ```
                depart = models.ForeignKey(verbose_name='所属部门',to="Department",db_constraint=False) # 无约束，但可以使用django orm的连表查询。

                    models.UserInfo.objects.filter(depart__title='xxx')
            ```
        * limit_choice_to
            - 连表只关联部分数据
                ```
                    class ClassList(models.Model):
                        """
                        班级表
                        """
                        title = models.CharField(verbose_name='班级名称', max_length=32)

                        bzr = models.ForeignKey(to=User,limit_choices_to={'id__lt':4})
                        teacher = models.ForeignKey(to=User,limit_choices_to={'id__gte':4})
                ```
        * related_name
            - 为外键设置别名，反向查询时，不用`表名_set`,而是通过related_name直接`.`字段

        + PS：对于fk，一般公司数据量和访问量不大时，创建fk做约束，反之以牺牲硬盘空间和代码量，来获取访问速度的提升(连表查询速度比单表查询速度要慢)

    - M2M 多对多，本质还是fk
        - 联合唯一  就是一条数据不允许重复出现相同的  在meta中配置unique_together=[field1,field2]
        - 联合索引  出现联合中的第一个条件，或全部出现才使用
        - 比如有多个孩子，和多种颜色、每个孩子可以喜欢多种颜色，一种颜色可以被多个孩子喜欢，对于双向均是可以有多个选择
        ```
            只有django会自动创建第三张表(场景：关系表只有boy和girl的id)：
                    class Boy(models.Model):
                        name = models.CharField(max_length=32)

                    class Girl(models.Model):
                        name = models.CharField(max_length=32)

                        boy = models.ManyToManyField('Boy')

            手动创建第三张表（场景：除了boy和girl的id以外，还需要其他字段）：
                class Boy(models.Model):
                    name = models.CharField(max_length=32)

                class Girl(models.Model):
                    name = models.CharField(max_length=32)

                class Boy2Girl(models.Model):
                    b = models.ForeignKey(to='Boy')
                    g = models.ForeignKey(to='Girl')

                    class Meta:
                        unique_together = (
                            ("b", "g"),
                        )
        ```
    - O2O 一对一
        - 子表从母表中选出一条数据一一对应，母表中选出来一条就少一条，子表不可以再选择母表中已被选择的那条数据
        ```
            class userinfo:
                        """
                        所有员工 (130)
                        """
                        name = 用户名
                        email = 邮箱
                        ...
                    class Admin:
                        """
                        给30个人开账号(30)，可以登录教务系统
                        """
                        username = 登录用户名
                        password ='密码'

                        user =  models.OneToOneField(to='userinfo')

        ```
    - **[应用场景](http://www.cnblogs.com/pythonxiaohu/p/5814247.html)**
    * 一对一：一般用于某张表的补充，比如用户基本信息是一张表，但并非每一个用户都需要有登录的权限，不需要记录用户名和密码，此时，合理的做法就是新建一张记录登录信息的表，与用户信息进行一对一的关联，可以方便的从子表查询母表信息或反向查询

    * 外键：有很多的应用场景，比如每个员工归属于一个部门，那么就可以让员工表的部门字段与部门表进行一对多关联，可以查询到一个员工归属于哪个部门，也可反向查出某一部门有哪些员工

    * 多对多：如很多公司，一台服务器可能会有多种用途，归属于多个产品线当中，那么服务器与产品线之间就可以做成对多对，多对多在A表添加manytomany字段或者从B表添加，效果一致


    >- choices的应用场景，当如性别等这些属性不随时间的推移发生个数的变化，可以将其放入内存代替放入数据库，这是一种数据库优化的手段。
    ```
        class Customer(models.Model):
                        name = models.CharField(verbose_name='姓名',max_length=32)
                        gender_choices = (
                            (1,'男'),
                            (2,'女'),
                        )
                        gender = models.IntegerField(choices=gender_choices)
    ```

3. **常用ORM操作**
    - 增
        1. models.Department.object.create(titel="xxx") or .create(`**`{"title":"xxx"})

        2. models.UserInfo.objects.create(depart=models.Department.bojects.get(id=1)) 增加一个关联对象

           model.Department.object.create(depart_id=1)

        3. obj = models.UserInfo.objects.filter(id=1).first()

           obj.roles.`add(*[1,2,3])`

    - 删
        1. obj.delete()

    - 改
        1. obj.update(name="xxx")
        2. obj.reles.set([2,3,4])

    - 查
        1. get()、filter()、exclude()、reverse()、distinct()、all()、values(field，field)、values_list(field)

4. 高级操作
    - **only**
    - 仅显示表中部分指定字段的数据，返回值为一个个对象，如果再用对象查其它字段会再次连接数据库，影响效率
    ```
        # queryset[obj,obj,obj] 返回值为一个个对象

        queryset = models.UserInfo.objects.all().only("id","username")
        # < QuerySet[ < UserInfo: 张三 >, < UserInfo: 李四 >, < UserInfo: 王五 >, < UserInfo: 赵六 >] >

        # 下面这种用法严重影响效率，因为email字段没有再queryset中，要查email就还需要再次连一次数据库
        for obj in queryset:
            print(obj.id, obj.username, obj.email)


        # queryset[{},{},{}]

        queryset = models.UserInfo.objects.all().values("id","username")
        # < QuerySet[{'id': 1, 'username': '张三'}, {'id': 2, 'username': '李四'}, {'id': 3, 'username': '王五'}, {'id': 4,'username': '赵六'}] >

        # queryset[(),(),()]

        queryset = models.UserInfo.objects.all().values_list("id","username")
        # < QuerySet[(1, '张三'), (2, '李四'), (3, '王五'), (4, '赵六')] >
    ```
    - **defer** 查询中排除某些字段，返回值通only，同样如果用得到的对象查排除的字段，会再次连接数据库

    - **select_related**
    - 主动进行连表查询，通过sql的join进行优化，会主动将关联字段一次性获取，这样当要查外键对象的属性时，不会再连数据库，而从内存拿，减少查询次数，提高了处理时间。
    ```
        select_related主要针一对一和多对一关系进行优化。
        select_related使用SQL的JOIN语句进行优化，通过减少SQL查询的次数来进行优化、提高性能。
        可以通过可变长参数指定需要select_related的字段名。也可以通过使用双下划线“__”连接字段名来实现指定的递归查询。没有指定的字段不会缓存，没有指定的深度不会缓存，如果要访问的话Django会再次进行SQL查询。
        也可以通过depth参数指定递归的深度，Django会自动缓存指定深度内所有的字段。如果要访问指定深度外的字段，Django会再次进行SQL查询。
        也接受无参数的调用，Django会尽可能深的递归查询所有的字段。但注意有Django递归的限制和性能的浪费。
        Django >= 1.7，链式调用的select_related相当于使用可变长参数。Django < 1.7，链式调用会导致前边的select_related失效，只保留最后一个。
    ```
    - **prefetch_related**
    - 多次单表查询，避免连表查询

    > 效能分析
        - 对比：
            方式一：

                result = models.User.objects.all() # 1次单表

                for row in result:
                    print(row.id,row.name,row.depart.title) # 100次单表

            方式二（小于4张表的连表操作）： ***

                result = models.User.objects.all().select_related('depart') # 1次连表查询
                for row in result:
                    print(row.id,row.name,row.depart.title)


            方式三（大于4张表连表操作）：

                # 先执行SQL： select * from user;
                # 在执行SQL： select * from depart where id in [11,20]
                result = models.User.objects.all().prefetch_related('depart') # 2次单表查询
                for row in result:
                    print(row.id,row.name,row.depart.title)

5. ORM操作原生sql三种方法
    - connection   直接操作数据库，本质是通过pymysql来操作，创建游标，执行sql语句，获取结果
    - connections  在上面的基础上多了个指定数据库的功能
    ```
        from jango.db import connection,connections
        # cursot = cursor.connections["db_name"].cursor() # 指定在setting中配置的数据库key
        cursor = connection.cursor()  # 建立游标
        cursor.execute("select * from goods where id=%s", [1,])  # 规定第二个参数要么是list，要么是tuple
    ```

    - raw 依赖model，执行sql语句,当查询其它表时，需要引用当前表的主键列名
    ```
        model.goos.objects.raw('select * from goos where id > 1')
    ```
    - extra 依赖model，执行部分sql，select或where，构造额外的查询条件或映射

>**所有ORM操作**
```
    ##################################################################
    # PUBLIC METHODS THAT ALTER ATTRIBUTES AND RETURN A NEW QUERYSET #
    ##################################################################

    def all(self)
        # 获取所有的数据对象

    def filter(self, *args, **kwargs)
        # 条件查询
        # 条件可以是：参数，字典，Q

    def exclude(self, *args, **kwargs)
        # 条件查询
        # 条件可以是：参数，字典，Q

    def select_related(self, *fields)
         性能相关：表之间进行join连表操作，一次性获取关联的数据。
         model.tb.objects.all().select_related()
         model.tb.objects.all().select_related('外键字段')
         model.tb.objects.all().select_related('外键字段__外键字段')

    def prefetch_related(self, *lookups)
        性能相关：多表连表操作时速度会慢，使用其执行多次SQL查询在Python代码中实现连表操作。
                # 获取所有用户表
                # 获取用户类型表where id in (用户表中的查到的所有用户ID)
                models.UserInfo.objects.prefetch_related('外键字段')

                from django.db.models import Count, Case, When, IntegerField
                Article.objects.annotate(
                    numviews=Count(Case(
                        When(readership__what_time__lt=treshold, then=1),
                        output_field=CharField(),
                    ))
                )

                students = Student.objects.all().annotate(num_excused_absences=models.Sum(
                    models.Case(
                        models.When(absence__type='Excused', then=1),
                    default=0,
                    output_field=models.IntegerField()
                )))

    def annotate(self, *args, **kwargs)
        # 用于实现聚合group by查询

        from django.db.models import Count, Avg, Max, Min, Sum

        v = models.UserInfo.objects.values('u_id').annotate(uid=Count('u_id'))
        # SELECT u_id, COUNT(ui) AS `uid` FROM UserInfo GROUP BY u_id

        v = models.UserInfo.objects.values('u_id').annotate(uid=Count('u_id')).filter(uid__gt=1)
        # SELECT u_id, COUNT(ui_id) AS `uid` FROM UserInfo GROUP BY u_id having count(u_id) > 1

        v = models.UserInfo.objects.values('u_id').annotate(uid=Count('u_id',distinct=True)).filter(uid__gt=1)
        # SELECT u_id, COUNT( DISTINCT ui_id) AS `uid` FROM UserInfo GROUP BY u_id having count(u_id) > 1

    def distinct(self, *field_names)
        # 用于distinct去重
        models.UserInfo.objects.values('nid').distinct()
        # select distinct nid from userinfo

        注：只有在PostgreSQL中才能使用distinct进行去重

    def order_by(self, *field_names)
        # 用于排序
        models.UserInfo.objects.all().order_by('-id','age')

    def extra(self, select=None, where=None, params=None, tables=None, order_by=None, select_params=None)
        # 构造额外的查询条件或者映射，如：子查询

        UserInfo.objects.extra(where=['headline ? %s'], params=['Lennon'])
        # select * from userinfo where headline > 'Lennon'

        UserInfo.objects.extra(where=["foo='a' OR bar = 'a'", "baz = 'a'"])
        # select * from userinfo where (foo='a' OR bar = 'a') and baz = 'a'

        UserInfo.objects.extra(select={'new_id': "select col from sometable where othercol > %s"}, select_params=(1,))
            """
            select
                id,
                name,
                (select col from sometable where othercol > 1) as new_id
            """
        UserInfo.objects.extra(select={'new_id': "select id from tb where id > %s"}, select_params=(1,), order_by=['-nid'])

     def reverse(self):
        # 倒序
        models.UserInfo.objects.all().order_by('-nid').reverse()
        # 注：如果存在order_by，reverse则是倒序，如果多个排序则一一倒序


     def defer(self, *fields):
        models.UserInfo.objects.defer('username','id')
        或
        models.UserInfo.objects.filter(...).defer('username','id')
        #映射中排除某列数据

     def only(self, *fields):
        #仅取某个表中的数据
         models.UserInfo.objects.only('username','id')
         或
         models.UserInfo.objects.filter(...).only('username','id')

     def using(self, alias):
         指定使用的数据库，参数为别名（setting中的设置）

         models.UserInfo.objects.filter(id=5).using('db1')


    ##################################################
    # PUBLIC METHODS THAT RETURN A QUERYSET SUBCLASS #
    ##################################################

    def raw(self, raw_query, params=None, translations=None, using=None):
        # 执行原生SQL
        models.UserInfo.objects.raw('select * from userinfo where id > 10 ')

        # 如果SQL是其他表时，必须将名字设置为当前UserInfo对象的主键列名
        models.UserInfo.objects.raw('select id as nid from 其他表')

        # 为原生SQL设置参数
        models.UserInfo.objects.raw('select id as nid from userinfo where nid>%s', params=[12,])

        # 将获取的到列名转换为指定列名
        name_map = {'first': 'first_name', 'last': 'last_name', 'bd': 'birth_date', 'pk': 'id'}
        Person.objects.raw('SELECT * FROM some_other_table', translations=name_map)

        # 指定数据库
        models.UserInfo.objects.raw('select * from userinfo', using="default")

    ################### 原生SQL ###################
    from django.db import connection, connections
    cursor = connection.cursor()  # cursor = connections['default'].cursor()
    cursor.execute("""SELECT * from auth_user where id = %s""", [1])
    row = cursor.fetchone() # fetchall()/fetchmany(..)


    def values(self, *fields):
        # 获取每行数据为字典格式

    def values_list(self, *fields, **kwargs):
        # 获取每行数据为元祖

    def dates(self, field_name, kind, order='ASC'):
        # 根据时间进行某一部分进行去重查找并截取指定内容
        # kind只能是："year"（年）, "month"（年-月）, "day"（年-月-日）
        # order只能是："ASC"  "DESC"
        # 并获取转换后的时间
            - year : 年-01-01
            - month: 年-月-01
            - day  : 年-月-日

        models.DatePlus.objects.dates('ctime','day','DESC')

    def datetimes(self, field_name, kind, order='ASC', tzinfo=None):
        # 根据时间进行某一部分进行去重查找并截取指定内容，将时间转换为指定时区时间
        # kind只能是 "year", "month", "day", "hour", "minute", "second"
        # order只能是："ASC"  "DESC"
        # tzinfo时区对象
        models.DDD.objects.datetimes('ctime','hour',tzinfo=pytz.UTC)
        models.DDD.objects.datetimes('ctime','hour',tzinfo=pytz.timezone('Asia/Shanghai'))

        """
        pip3 install pytz
        import pytz
        pytz.all_timezones
        pytz.timezone(‘Asia/Shanghai’)
        """

    def none(self):
        # 空QuerySet对象


    ####################################
    # METHODS THAT DO DATABASE QUERIES #
    ####################################

    def aggregate(self, *args, **kwargs):
       # 聚合函数，获取字典类型聚合结果
       from django.db.models import Count, Avg, Max, Min, Sum
       result = models.UserInfo.objects.aggregate(k=Count('u_id', distinct=True), n=Count('nid'))
       ===> {'k': 3, 'n': 4}

    def count(self):
       # 获取个数

    def get(self, *args, **kwargs):
       # 获取单个对象

    def create(self, **kwargs):
       # 创建对象

    def bulk_create(self, objs, batch_size=None):
        # 批量插入
        # batch_size表示一次插入的个数
        objs = [
            models.DDD(name='r11'),
            models.DDD(name='r22')
        ]
        models.DDD.objects.bulk_create(objs, 10)

    def get_or_create(self, defaults=None, **kwargs):
        # 如果存在，则获取，否则，创建
        # defaults 指定创建时，其他字段的值
        obj, created = models.UserInfo.objects.get_or_create(username='root1', defaults={'email': '1111111','u_id': 2, 't_id': 2})

    def update_or_create(self, defaults=None, **kwargs):
        # 如果存在，则更新，否则，创建
        # defaults 指定创建时或更新时的其他字段
        obj, created = models.UserInfo.objects.update_or_create(username='root1', defaults={'email': '1111111','u_id': 2, 't_id': 1})

    def first(self):
       # 获取第一个

    def last(self):
       # 获取最后一个

    def in_bulk(self, id_list=None):
       # 根据主键ID进行查找
       id_list = [11,21,31]
       models.DDD.objects.in_bulk(id_list)

       models.User.objects.filter(id__in=[11,21,31])

    def delete(self):
       # 删除

    def update(self, **kwargs):
        # 更新

    def exists(self):
       # 是否有结果
```


## Form，model.Form，modelForm.set
 - 返回时通过form生成表单标签，用户输入信息发给后台，通过form来进行校验，有异常返回错误信息，并保存用户数据，然后保存到数据库


## 简叙session和cookie？
- django的session是，用户第一次访问验证后，服务端会在后台生成一个随机字符串sessionid通过设置响应头set-cookit返回给浏览器，当浏览器下次再次请求时会自动带上随机字符串存放在cookie中，服务端拿到浏览器的session与数据库中的进行比对，从而获得用户状态。

- 底层实现：
    - django接到请求，在中间件process_reqeust方法中，在内存中设置一个空字典，之后在视图中通过reqeust.session[key] 的方式设置session（本质是调用类中的setitem方法），返回时在中间件的process_response方法中，将字典存放到数据库，sessionid为key，设置的用户的数据为value存放到数据库，然后通过设置cookie的方法response.set_cookie将sessionid也就是随机字符串存放到响应头set_cookie中，返回到浏览器，浏览器保存到本地。下次访问时浏览器自定将sessionid存在cookie中发送过来，经过中间件，同样process_request方法从数据库中获取session进行比对，从而确认用户状态。


## RBAC 基于角色的权限控制
> 权限中都有哪些表、表和表之间的关系
    - 6张表，用户表、角色表、权限表、权限角色表、用户角色表、菜单表
    - 用户与角色 多对多
    - 权限与角色 多对多
    - 菜单与权限 一对多  （一个一级菜单有多个二级菜单即有多个权限）
>> ps：菜单表  目的：为了做二级菜单，它存放的是一级菜单，权限表里对应到菜单表，它存放的是菜单下的子菜单

难忘点：

- 一个`/` 录入权限时，如果没有在路径前面加/，而程序中也没有进行处理拼接，就会导致除了白名单外，所有的权限丢被阻止！！！！

## 简述权限组件的实现流程？
- 在web中，一个url就是一个权限
- 用户访问经过实现wsgi协议wsgiref模块，进入中间件，经过自定义的访问权限验证中间件的process_request方法，通过设置白名单，允许通用的权限通过不用验证，如注册、登录，其它的都需要通过验证才能访问。
- 具体实现为，用户第一次登录验证成功后，根据用户的角色将用户的权限封装到session中，返回给用户存放到本地，
下次用户访问带上session，经过中间件进行循环验证，通过则继续通过路由系统匹配对应的视图，返回html字符串给浏览器渲染。
- 菜单也是权限，在初始化用户权限时，将菜单也一样封装到session中，在中间件验证通过后，路由匹配视图返回响应时，获取session中的菜单信息，循环动态生成菜单。

- 缺点：这种在登录后将用户的权限写入session的缺点是，用户登录后，如果给用户添加了权限，需要用户退出后，再次登录才能有权限，无法实时更新！！！

- 权限控制到按钮级别，就是看该按钮的url在不在权限字典中。有就生成！
```
permission_dict = {
    url别名：{
        title：xxx，
        url：/
    }
}

```

##
- 用户表
- 角色表
- 用户角色表

- 权限表
- 权限角色表

- 菜单表  目的：为了做二级菜单，它存放的是一级菜单
- 菜单权限表


# djangorestframework  api接口框架
## 使用
1. 安装
```
pip3 install djangorestframework
```
2. 创建路由 `url(r'test/', view.Test.as_view(), name="test")`

3. 创建视图，继承APIVIEW
```python


```
