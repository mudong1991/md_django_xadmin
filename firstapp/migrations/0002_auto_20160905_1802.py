# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-05 18:02
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookborrowinfo',
            name='standard_return_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 9, 8, 18, 2, 50, 100000)),
        ),
    ]
