from django.contrib import admin
from Rbac import models

for table in models.__all__:
    admin.site.register(getattr(models, table))


















# from django.contrib import admin
# from rbac import models
#
# admin.site.register(models.Menu)
#
#
# class PermissionAdmin(admin.ModelAdmin):
#     list_display = ['id','title', 'url','name' ]
#     list_editable = ['url', 'name']
#
#
# admin.site.register(models.Permission, PermissionAdmin)
# admin.site.register(models.Role)
# admin.site.register(models.UserInfo)
