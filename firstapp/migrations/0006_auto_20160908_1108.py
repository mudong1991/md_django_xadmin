# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-08 11:08
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0005_auto_20160906_1732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookborrowinfo',
            name='standard_return_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 9, 11, 11, 8, 37, 742000)),
        ),
    ]
