# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-03 20:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0021_auto_20170104_0028'),
    ]

    operations = [
        migrations.DeleteModel(
            name='alerts',
        ),
    ]