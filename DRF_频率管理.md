# DRF_访问频率的管理
## 自定义创建频率类
1. 继承object类
2. 必须重写方法allow_request(self,request,view)，返回值必须是bool
3. 必须有wait()方法，返回值为int，表示还要等多久才可访问

## 配置
        全局：
            在settings.py文件中设置：
            REST_FRAMEWORK = {
                'DEFAULT_THROTTLE_CLASSES':[自定义频率控制类的path],
            }

        局部：
            直接在某个视图中应用,settings.py中无需配置
            1. 先导入自定义的频率控制类
            2. 在视图中配置：throttle_classes = [MyThrottle]
### 示例
```
全局应用==> 需求：规定60秒内最多访问5次

--MyThrottle.py

    import time
    class MyThrottle(object):
        """
        {
        {IP:[t1,t2,t3]}
        {IP2:[t1,t2,t3]}
        }
        """

        def __init__(self):
            self.history = None
            self.timer = time.time

        def allow_request(self, request, view):
            """返回值必须是True/False"""
            ip = request.META.get("REMOTE_ADDR", "")
            # 如果ip不存在，则增
            if ip not in visit_record:
                visit_record[ip] = [self.timer(), ]
            history = visit_record[ip]
            self.history = history
            # 如果存在,确保列表中存放的时间是单位时间内的
            while self.history and self.timer() - self.history[-1] > 60:
                self.history.pop()
            # 维护好时间，判断访问次数
            if len(self.history) + 1 >= 3:
                return False
            else:
                self.history.insert(0, self.timer())
                return True

        def wait(self):
            """必须是返回int"""
            return 60 - (self.timer() - self.history[-1])
```
```
--settings.py
    REST_FRAMEWORK = {
        'DEFAULT_THROTTLE_CLASSES': ['demo_auth.MyThrottle.MyThrottle'],
    }
```
```
局部应用==>

--views.py

    1. 导入自己写的MyThrottle
        from demo_auth.MyThrottle import MyThrottle
    2. 配置
    class T(APIView):
        throttle_classes = [MyThrottle]

        def get(self,request):
            return Response("测试中")
```

## 应用DRF框架的频率控制类
1. 创建自己的控制类，继承框架提供的类，如 from rest_framework.throttling import SimpleRateThrottle
2. 类中必须重写get_cache_key(self,request,view)方法，获取以什么为参照，管控用户的访问
3. 类中必须配置scope变量，用于获得频率的参数，如5/m  表示1分钟只能访问5次

## 配置
        全局：
            在settings.py文件中设置：
            REST_FRAMEWORK = {
                'DEFAULT_THROTTLE_CLASSES':[自定义频率控制类的path],
                'DEFAULT_THROTTLE_RATES': {"SM": "5/m"}
            }

        局部：
            直接在某个视图中应用
            1. 先导入自定义的频率控制类
            2. 在视图中配置：throttle_classes = [MyThrottle]
            3. 在控制类中必须配置THROTTLE_RATES值是一个字典，内容为频率的参数

```
全局应用==>

--MyThrottle.py

    from rest_framework.throttling import SimpleRateThrottle

    class GlobalsThrottle(SimpleRateThrottle):
        scope = "SM"

        def get_cache_key(self, request, view):
            return self.get_ident(request)
```
```
--settings.py
    REST_FRAMEWORK = {
        'DEFAULT_THROTTLE_CLASSES': ['demo_auth.MyThrottle.MyThrottle'],
        'DEFAULT_THROTTLE_RATES': {"SM": "5/m"}
    }
```
```
局部应用==>
--MyThrottle.py

    from rest_framework.throttling import SimpleRateThrottle

    class GlobalsThrottle(SimpleRateThrottle):
        THROTTLE_RATES = {"SM": "5/m"}  # 局部重点配置这个选项
        scope = "SM"

        def get_cache_key(self, request, view):
            return self.get_ident(request)

--views.py

    1. 导入自己写的MyThrottle
        from demo_auth.MyThrottle import MyThrottle
    2. 配置
    class T(APIView):
        throttle_classes = [MyThrottle]

        def get(self,request):
            return Response("测试中")
```

>**源码：**
    def check_throttles(self, request):
        """
        Check if request should be throttled.
        Raises an appropriate exception if the request is throttled.
        """
        for throttle in self.get_throttles():
            if not throttle.allow_request(request, self):
                self.throttled(request, throttle.wait())

### 源码解析：
1. 视图继承APIVIEW类，url匹配视图，执行as_view方法，APIVIEW类重写as_view方法，在继承了View的as_view方法的基础上，实现了豁免csrf，实现每个视图不被拦截
View类的as_view方法，最终返回view方法，view方法会执行APIVIEW重写的dispatch方法（同时也重新封装request对象），更具请求不同进行分发，执行对应视图函数;
2. 分流控制，通过check_throttles(view,request)方法，进行分流管理;

>
    - 首先通过get_throttles()方法获取setting中配置的控制类，进行实例化，组成列表返回;
    - 然后遍历每个控制类实例化对象，执行类中配置处理分流逻辑的allow_request方法，返回值为bool；
    - 最后不符合规则的访问执行throttled()方法，调用类中定义的wait()方法，展示还需等待多久才能访问信息；


