# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-08-18 18:54
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('rememberTheCheese', '0005_auto_20160816_1247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 21, 18, 54, 32, 692619, tzinfo=utc), verbose_name='deadline'),
        ),
        migrations.AlterField(
            model_name='lista',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2016, 9, 2, 18, 54, 32, 403416, tzinfo=utc), verbose_name='deadline'),
        ),
    ]