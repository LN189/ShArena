# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-01 05:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_groups', '0010_remove_textfile_pro'),
    ]

    operations = [
        migrations.AddField(
            model_name='textfile',
            name='pro',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
