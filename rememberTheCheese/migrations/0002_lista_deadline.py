# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-08-16 12:20
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('rememberTheCheese', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lista',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 16, 12, 20, 45, 882224, tzinfo=utc), verbose_name='deadline'),
        ),
    ]
