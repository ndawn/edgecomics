# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-03 11:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('previews', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='preview',
            name='diamond_code',
        ),
        migrations.AddField(
            model_name='preview',
            name='diamond_id',
            field=models.CharField(max_length=16, null=True, verbose_name='ID Diamond'),
        ),
    ]
