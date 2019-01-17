from django.db import models

__all__ = ["UserInfo", "Role", "Permission", "Menu"]


# Create your models here.
class UserInfo(models.Model):
    """
    用户表
    """
    username = models.CharField(verbose_name="用户名", max_length=32, unique=True)
    password = models.CharField(verbose_name="密码", max_length=32)
    role = models.ManyToManyField(verbose_name="所属角色", to="Role")

    class Meta:
        verbose_name_plural = "用户表"

    def __str__(self):
        return self.username


class Role(models.Model):
    """
    角色表
    """
    name = models.CharField(verbose_name="角色名", max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "角色表"


class Menu(models.Model):
    """
    菜单表
    unique 唯一，不能重复
    db_index 创建索引，便于快速
    """
    title = models.CharField(verbose_name="菜单名", max_length=32, )
    icon = models.CharField(verbose_name="图标", max_length=32)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "菜单表"


class Permission(models.Model):
    """
    权限名
    权限与菜单多对一 blank表示admin可以为空
    """
    url = models.CharField(verbose_name="url地址", max_length=32)
    title = models.CharField(verbose_name="权限名", max_length=32, null=True)
    name = models.CharField(verbose_name="url别名", max_length=32)
    role = models.ManyToManyField(verbose_name="所属角色", to="Role")
    menu = models.ForeignKey(verbose_name="所属菜单", to="Menu", null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "权限表"
