# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-01 23:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0007_auto_20171001_2313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('requested', 'Requested'), ('progressing', 'Progressing'), ('done', 'Done')], default='requested', max_length=32),
        ),
    ]
