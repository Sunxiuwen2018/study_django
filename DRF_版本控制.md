# DRF_版本控制
## 使用自定义的版本控制类
1. 继承版本控制基类BaseVersioning
2. 重写自己的`determine_version(self, request, *args, **kwargs)`方法

>注：一般进行版本控制要么将版本信息放在url，header，hostname，namespace命名空间上，系统提供足以满足要求

## 配置【以将版本信息放在url上举例】
    全局：
        - 在setting中配置默认认证管理类：
            REST_FRAMEWORK = {
            # 默认的版本控制类
            'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
            # 默认的使用版本
            'DEFAULT_VERSION': ['v1', 'v2'],
            # 允许的版本
            # 'ALLOWED_VERSIONS': 'v2',
            'ALLOWED_VERSIONS': ['v1', 'v2'],
            # 版本使用的参数名称
            'VERSION_PARAM': 'version',}
        - 在urls.py上配置：
            urlpatterns = [
                        url(r'(?P<version>[v1|v2]+)/api/', views.TestView.as_view())，]

    局部：直接在视图中配置：versioning_class = [MyVersion]，如果要局部需在认证类中，指定好全局中配置的各项参数

## 示例
```
--views.py

    class TestView(APIView):
        def get(self, request, *args, **kwargs):
            # 认证通过后会将版本信息和版本实例化对象封装到request对象
            print(request.versioning_scheme)
            # 获得版本对象<rest_framework.versioning.URLPathVersioning object at 0x000002A1137D4B00>
            print(request.version)
            # 获取版本号
            ret = request.version
            if ret == "v1":
                return Response("版本v1的信息")
            elif ret == "v2":
                return Response("版本v2的信息")  # 此时无法显示，因版本控制里只有设置v1允许
            else:
                return Response("没有匹配不到")
```
>**源码**

        def initial(self, request, *args, **kwargs):
            # 版本
            version, scheme = self.determine_version(request, *args, **kwargs)
            request.version, request.versioning_scheme = version, scheme

        def determine_version(self, request, *args, **kwargs):
            """
            If versioning is being used, then determine any API version for the
            incoming request. Returns a two-tuple of (version, versioning_scheme)
            """
            if self.versioning_class is None:
                return (None, None)
            scheme = self.versioning_class()  # versioning_scheme是配置的版本控制类，加括号进行实例化
            return (scheme.determine_version(request, *args, **kwargs), scheme)  # 实例化对象调用自己的版本控制类方法，返回版本信息version

### 源码解析：
1. 视图继承APIVIEW类，url匹配视图，执行as_view方法，APIVIEW类重写as_view方法，在继承了View的as_view方法的基础上，实现了豁免csrf，实现每个视图不被拦截
View类的as_view方法，最终返回view方法，view方法会执行APIVIEW重写的dispatch方法（同时也重新封装request对象），更具请求不同进行分发，执行对应视图函数
2. 版本控制，通过determine_version方法管理版本，返回值为request.version,request.versioning_scheme,封装到request对象上

>
    - 首先通过versioning_class()获取setting配置中版本控制类，并进行实例化
    - 然后执行自己版本控制类中的determine_version方法，返回version信息
    - 最后将版本信息version和版本控制类实例化对象赋值给request对象

---
### 版本源码流程
```
url-->CBV视图-->继承APIVIEW类-->执行APIVIEW类中的as_view()--> csrf_exempt(view)豁免所有post请求的csrf放回view函数-->执行父类得view函数
    -->执行APIVIEW类中dispatch方法
    -->执行self.initialize_request(request, *args, **kwargs)重新封装request-->执行inital初始化方法
    ==》version, scheme = self.determine_version(request, *args, **kwargs)获取版本，及版本控制类对象
    ==》实例化版本类对象赋值给scheme【scheme = self.versioning_class()】，执行版本控制类中的determine_version方法，return version
    ==》对获取的版本信息和对象进行解构重新赋值
    ==》再次面向对象为request对象，将两个属性添加给request【 request.version, request.versioning_scheme = version, scheme】
    ==》之后就可以通过request操作版本信息了
```
