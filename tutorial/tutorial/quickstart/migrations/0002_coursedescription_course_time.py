# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-06 00:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursedescription',
            name='course_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]