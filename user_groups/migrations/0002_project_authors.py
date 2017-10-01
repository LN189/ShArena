# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-30 10:19
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_groups', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='authors',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
