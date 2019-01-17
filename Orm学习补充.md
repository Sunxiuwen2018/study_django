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



[vue-cli3](https:://blog.csdn.net/qq_36407748/article/details/80739787 "Markdown")

[虚拟环境](https:://blog.csdn.net/weixin_39036700/article/details/80711565?utm_source=blogxgwz0 "Markdown")








