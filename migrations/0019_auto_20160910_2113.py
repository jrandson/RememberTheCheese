# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-10 21:13
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('rememberTheCheese', '0018_auto_20160910_2112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subtask',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2016, 9, 13, 21, 13, 51, 187678, tzinfo=utc), verbose_name='deadline'),
        ),
        migrations.AlterField(
            model_name='task',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2016, 9, 13, 21, 13, 51, 186045, tzinfo=utc), verbose_name='deadline'),
        ),
    ]
