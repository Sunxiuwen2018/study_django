# Serializer 序列化后的数据放在data方法里

## 1、通过序列化器，序列化后的数据放在data里

>url-->CBV视图-->继承APIVIEW类-->执行APIVIEW类中的as_view()
    -->执行APIVIEW类中dispatch方法-->执行self.initialize_request(request, *args, **kwargs)重新封装request-->执行inital初始化方法
    ==》version, scheme = self.determine_version(request, *args, **kwargs)获取版本，及版本控制类对象
    ===》实例化版本类对象赋值给scheme【scheme = self.versioning_class()】，执行版本控制类中的determine_version方法，return version
    ==》对获取的版本信息和对象进行解构重新赋值
    ==》再次面向对象为request对象，将两个属性添加给request【 request.version, request.versioning_scheme = version, scheme】
    ==》之后就可以通过request操作版本信息了


