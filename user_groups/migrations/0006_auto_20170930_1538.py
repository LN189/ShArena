# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-30 15:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_groups', '0005_textfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='textfile',
            name='document',
            field=models.FileField(upload_to='user_/'),
        ),
    ]
