# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-21 12:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lendingapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ledger',
            name='interest',
            field=models.FloatField(default=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='credit',
            name='dt',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='ledger',
            name='dt',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='payment',
            name='dt',
            field=models.DateField(),
        ),
    ]
