# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-07-18 11:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showsearch', '0005_auto_20180718_1711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tvshow',
            name='rating',
            field=models.CharField(blank=True, max_length=5),
        ),
    ]
