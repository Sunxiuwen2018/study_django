# DRF_权限管理
## 自定义创建权限管理
1. 导入权限管理基类，继承基类BasePermission
2. 必须重写has_permissions(request.view)方法，用户权限校验逻辑，返回值必须时bool
3. 必须有message变量，用于当无权限时返回提示信息

## 配置
    全局在settings中配置默认权限管理类为自定义的类：'DEFAULT_PERMISSION_CLASSES':["demo_permissions.MyPermissions.MyPermission"],
    局部直接在指定视图中指定权限管控类：permission_classes = [MyPermission]

## 示例

```
-- MyPermissions.py

    from rest_framework.permissions import BasePermission


    class MyPermission(BasePermission):
        """
        权限管控是为了对事物的决策和范围进行一种管理，
        不同的权限能做不同的事
        权限是在认证之后发生的事，必须先认证了，才有权限的事，
        认证过后，就可以得到认证对象，和认证用户
        """
        message = "没有权限"

        def has_permission(self, request, view):
            """request已经封装，request.data,request.query_params
                认证后返回了request.user包含认证后的用户信息 ！！！
                返回值只可能为bool
                主要做的事就是判断对象是否有某个权限，有返回true，反之false
                为用户设定权限是通过角色来定，修改models
            """
            if request.user and request.user.type == 2:
                return True
            else:
                return False
```
>全局
    --settings.py
        REST_FRAMEWORK = {
            'DEFAULT_PERMISSION_CLASSES': ["demo_permissions.MyPermissions.MyPermission"],
        }

>局部
    --views.py
        from demo_permissions.MyPermissions import MyPermission
        class TestView(APIView):
            permission_classes = [MyPermission]
            def get(self, request):
                return Response("测试中")

>**源码**

    def check_permissions(self, request):
        """
        Check if the request should be permitted.
        Raises an appropriate exception if the request is not permitted.
        """
        for permission in self.get_permissions():
            if not permission.has_permission(request, self):
                # self是视图
                self.permission_denied(
                    request, message=getattr(permission, 'message', None)
                )
### 源码解析：
1. 视图继承APIVIEW类，url匹配视图，执行as_view方法，APIVIEW类重写as_view方法，在继承了View的as_view方法的基础上，实现了豁免csrf，实现每个视图不被拦截
View类的as_view方法，最终返回view方法，view方法会执行APIVIEW重写的dispatch方法（同时也重新封装request对象），更具请求不同进行分发，执行对应视图函数
2. 权限控制，是在通过认证过后通过check_permissions(view,request)方法进行管理

>
    - 是先通过get_permissions()方法获取setting中配置的控制类，进行实例化，组成列表返回;
    - 然后遍历各个权限控制类实例化对象,让其执行权限控制类中处理权限逻辑的has_permission(request, view)方法，返回值为bool；
    - 如果没有权限，就走permission_denied，反射获取message变量设置好的没有权限的报错信息；
