# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-08-26 18:18
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('rememberTheCheese', '0013_auto_20160825_1441'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='closed',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='subtask',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 29, 18, 18, 5, 516635, tzinfo=utc), verbose_name='deadline'),
        ),
        migrations.AlterField(
            model_name='task',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 29, 18, 18, 5, 245908, tzinfo=utc), verbose_name='deadline'),
        ),
    ]
