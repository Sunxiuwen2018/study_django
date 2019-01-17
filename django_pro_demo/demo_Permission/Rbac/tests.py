from django.test import TestCase

# Create your tests here.
#  在应用的目录下建立一个py文件，将下面的代码写入
import os

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Permission.settings")
    import django
    django.setup()

    from Rbac import models

    '''所有的orm操作写在此处'''
    queryset = models.UserInfo.objects.all().only("id","username")
    # < QuerySet[ < UserInfo: 张三 >, < UserInfo: 李四 >, < UserInfo: 王五 >, < UserInfo: 赵六 >] >
    queryset = models.UserInfo.objects.all().values("id","username")
    # < QuerySet[{'id': 1, 'username': '张三'}, {'id': 2, 'username': '李四'}, {'id': 3, 'username': '王五'}, {'id': 4,
    #                                                                                                    'username': '赵六'}] >
    queryset = models.UserInfo.objects.all().values_list("id","username")
    # < QuerySet[(1, '张三'), (2, '李四'), (3, '王五'), (4, '赵六')] >
    print(queryset)
    from django.db import connections,connection
    cursor = connection.cursor()
    cursor.execute("""select * from auth_user where id=%s""", (1,))
    print(cursor.fetchone())
    # ret = models.UserInfo.objects.filter(username="xiuwensun@163.com").delete()
    # print(ret)

