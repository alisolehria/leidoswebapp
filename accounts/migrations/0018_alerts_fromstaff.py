# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-03 20:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_remove_alerts_fromstaff'),
    ]

    operations = [
        migrations.AddField(
            model_name='alerts',
            name='fromStaff',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='accounts.profile'),
            preserve_default=False,
        ),
    ]
