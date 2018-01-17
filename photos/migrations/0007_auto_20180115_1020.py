# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-15 09:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0006_comment_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='photo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='photos.Photo'),
        ),
    ]