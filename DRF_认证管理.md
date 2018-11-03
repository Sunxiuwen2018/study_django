# DRF_认证管理
## 自定创建认证管理类
1. 导入基类，继承基类BaseAuthentication
2. 必须重写authenticate方法，用于处理认证逻辑

## 配置
    全局：在setting中配置默认认证管理类：'DEFAULT_AUTHENTICATION_CLASSES': ["demo_auth.MyAuth.MyAuthentication", ]
    局部：直接在视图中配置：authentication_classes = [MyAuthentication]

## 示例
```
--MyAuth.py

    from rest_framework.exceptions import APIException
    from rest_framework.authentication import BaseAuthentication
    from demo_auth import models


    class MyAuthentication(BaseAuthentication):

        def authenticate(self, request):
            """
            请求进入到视图里，先进行验证token
            必须定义此方法，拿到token验证,token是放在url上
            返回值必须是一个元组：一个用户对象，一个是验证的key
            """
            token = request.query_params.get("token", "")
            if not token:
                raise APIException(detail="缺少token", code=1001)
            user_obj = models.UserInfo.objects.filter(token=token).first()
            if user_obj:
                return user_obj, token
            else:
                raise APIException(detail="无效的token", code=1002)
```

>全局：
    --settings.py
        REST_FRAMEWORK = {
            'DEFAULT_AUTHENTICATION_CLASSES': ["demo_auth.Myauth.MyAuthentication", ],
        }

>局部：
    --views.py
        from demo_auth.MyAuth import MyAuthentication
        class TestView(APIView):
            authentication_classes = [MyAuthentication]
            def get(self, request):
                return Response("测试中")

>**源码**

    def perform_authentication(self, request):
        """
        Perform authentication on the incoming request.
        Note that if you override this and simply 'pass', then authentication
        will instead be performed lazily, the first time either
        `request.user` or `request.auth` is accessed.
        """
        request.user  # 返回封装后的request对象调用Request类中的user方法，拿到用户的所有信息

    def initialize_request(self, request, *args, **kwargs):
        """
        Returns the initial request object.
        """
        parser_context = self.get_parser_context(request)
        return Request(
            request,
            parsers=self.get_parsers(),
            authenticators=self.get_authenticators(),
            negotiator=self.get_content_negotiator(),
            parser_context=parser_context
        )

    --Request(object):
        @property
        def user(self):
            """
            Returns the user associated with the current request, as authenticated
            by the authentication classes provided to the request.
            """
            if not hasattr(self, '_user'):
                with wrap_attributeerrors():
                    self._authenticate()
            return self._user

        def _authenticate(self):
        """
        Attempt to authenticate the request using each authentication instance
        in turn.
        """
        for authenticator in self.authenticators:
        # 循环获取setting中配置的认证类的实例化对象组成的列表
            try:
                user_auth_tuple = authenticator.authenticate(self)
            except exceptions.APIException:
                self._not_authenticated()
                raise

### 源码解析：
1. 视图继承APIVIEW类，url匹配视图，执行as_view方法，APIVIEW类重写as_view方法，在继承了View的as_view方法的基础上，实现了豁免csrf，实现每个视图不被拦截
View类的as_view方法，最终返回view方法，view方法会执行APIVIEW重写的dispatch方法（同时也重新封装request对象），更具请求不同进行分发，执行对应视图函数
2. 认证管理，通过perform_authentication方法，返回request.user，包含用户的所有的信息，因此可以在认证后，其它地方通过reques.user获取用户的相关信息

>
    - 通过在setting中设置认证类，然后通过Request类重新封装request时通过get_authenticators()获取，并实例化放在一个列表中赋值给authenticators
    - 然后在Request类的user方法中通过_authenticate()循环authenticators，让每个认证类实例化对象执行处理认证逻辑的authenticate方法，
    - 最后返回一个包含user对象，和auth认证 的元组，最后将user，auth都赋值给request对象，使之称为request的属性，能够通过request对象调用