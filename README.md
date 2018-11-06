# 第一部分：Django回顾
## 简叙http协议？
```
Http协议全称为超文本传输协议，是基于tcp/ip协议进行通信的，它的显著特点是无状态，短连接，主要表现为服务端处理一次请求就会断开连接，且不保存用户状态，也就是说，客户端请求响应后，再次发送请求时，服务端还是不认识客户端，解决的方式之一就是建立session在服务端保存状态。再就是http的请求报文格式和响应报文格式主要都分为两部分请求头和请求体，响应头和响应体，请求头与请求头，响应头与响应头之间通过\r\n分割，请求头与请求体，响应头与响应体之间通过2个\r\n分割。
再就是常见的get请求是没有请求体的，它的数据是拼接在url上的，而post请求是放在请求体中的。
```
## 你了解的请求头都有哪些？
1. ACCEPT: 告诉服务端浏览器能够解析的数据格式
2. User-Agent： 告诉服务器浏览器的设备信息，如是什么浏览器，版本等等
3. referer： 存放来源地址告诉服务器是从那里来的，可以用作防盗链
4. host: 当前访问的主机名称
5. Conten-type：请求提交的数据格式，一般用于post/put/patch请求
6. Cookie： 将cookie信息带给服务器

## 你了解的响应头有哪些？
1. Conten-type：告知浏览器响应的数据格式
2. Server：告知浏览器，服务器的类型，如nginx等等
3. Location: 告知服务器找谁，一般重定向，会在这里显示要去的url，redirect的本质就是在响应中加了一个Location响应头
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

>>注：默认渲染的本质是将模板中特殊的标签，进行字符串的替换
>>必须会画django请求生命周期图

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

## 路由系统
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

## 视图系统
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

```
代码演练
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

## 模板系统
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
4.



