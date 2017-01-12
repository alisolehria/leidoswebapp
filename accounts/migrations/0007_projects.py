# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-26 20:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_profile_salary'),
    ]

    operations = [
        migrations.CreateModel(
            name='projects',
            fields=[
                ('projectID', models.AutoField(primary_key=True, serialize=False)),
                ('projectName', models.CharField(max_length=200)),
                ('startDate', models.DateField()),
                ('endDate', models.DateField()),
                ('description', models.TextField()),
                ('budget', models.IntegerField()),
                ('numberOfStaff', models.IntegerField()),
                ('status', models.CharField(choices=[(b'Pending Approval', b'Pending Approval'), (b'Approved', b'Approved'), (b'On Going', b'On Going'), (b'Completed', b'Completed'), (b'Declined', b'Declined'), (b'Discontinued', b'Discontinued')], max_length=30)),
                ('projectManager', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='accounts.profile')),
                ('staffID', models.ManyToManyField(to='accounts.profile')),
            ],
            options={
                'db_table': 'projects',
            },
        ),
    ]