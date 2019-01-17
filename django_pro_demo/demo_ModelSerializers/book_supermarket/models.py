from django.db import models

# Create your models here.
__all__ = ["User", "Book", "Publisher"]

BOOK_CATEGORY_CHOICE_LIST = (
    (1, "言情"),
    (2, "励志"),
    (3, "玄幻"),
    (4, "战争"),
)


class User(models.Model):
    """
    用户表
    token 为认证的密钥，用户登录后返回一个token，下次访问其它页面带上token，就可以识别用户，无需再登录
    还有一小点，uuid字段
    """
    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)
    token = models.UUIDField(verbose_name="密钥", null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = "用户表"


class Book(models.Model):
    """
    图书表
    """
    title = models.CharField(verbose_name="书名", max_length=32)
    pub_time = models.DateTimeField(verbose_name="出版时间")
    category = models.IntegerField(verbose_name="图书种类", choices=BOOK_CATEGORY_CHOICE_LIST)
    publisher = models.ForeignKey(verbose_name="出版社", to="Publisher")
    author = models.ManyToManyField(verbose_name="作者", to="User")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "图书表"


class Publisher(models.Model):
    """
    出版社表
    """
    title = models.CharField(verbose_name="出版社名称", max_length=32)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "出版社表"
