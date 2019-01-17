from django.contrib import admin
# user:cmdb@mail.com  pwd:cmdb123456
# Register your models here.
from assets import models


class NewAssetAdmin(admin.ModelAdmin):
    """新资产"""
    list_display = ['asset_type', 'sn', 'model', 'manufacturer', 'c_time', 'm_time']
    list_filter = ['asset_type', 'manufacturer', 'c_time']
    search_fields = ('sn',)


class AssetAdmin(admin.ModelAdmin):
    list_display = ['asset_type', 'name', 'status', 'approved_by', 'c_time', 'm_time']


admin.site.register(models.NewAssetApprovalZone, NewAssetAdmin)

for table in models.__all__:
    admin.site.register(getattr(models, table))
