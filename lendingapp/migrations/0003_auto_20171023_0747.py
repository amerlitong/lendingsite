# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-23 04:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lendingapp', '0002_auto_20171021_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ledger',
            name='interest',
            field=models.FloatField(null=True),
        ),
    ]
