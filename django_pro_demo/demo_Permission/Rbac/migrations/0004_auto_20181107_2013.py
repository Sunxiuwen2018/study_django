# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-11-07 12:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Rbac', '0003_auto_20181107_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permission',
            name='title',
            field=models.CharField(max_length=32, null=True, verbose_name='权限名'),
        ),
        migrations.AlterModelTable(
            name='userinfo',
            table=None,
        ),
    ]
