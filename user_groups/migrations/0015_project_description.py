# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-25 08:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_groups', '0014_auto_20171024_1401'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='description',
            field=models.TextField(default='', max_length=400),
        ),
    ]
