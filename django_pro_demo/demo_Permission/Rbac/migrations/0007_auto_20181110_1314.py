# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-11-10 05:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Rbac', '0006_auto_20181107_2025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='username',
            field=models.CharField(max_length=32, unique=True, verbose_name='用户名'),
        ),
    ]
