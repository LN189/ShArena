# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-30 10:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_groups', '0003_auto_20170930_1023'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='author',
            new_name='authors',
        ),
    ]