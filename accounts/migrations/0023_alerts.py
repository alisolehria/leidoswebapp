# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-03 20:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0022_delete_alerts'),
    ]

    operations = [
        migrations.CreateModel(
            name='alerts',
            fields=[
                ('alertID', models.AutoField(primary_key=True, serialize=False)),
                ('alertType', models.CharField(choices=[(b'Project', b'Project'), (b'Leave', b'Leave'), (b'Staff', b'Staff')], max_length=30)),
                ('alertDate', models.DateField()),
                ('status', models.CharField(choices=[(b'Seen', b'Seen'), (b'Unseen', b'Unseen')], max_length=30)),
                ('seenDate', models.DateField(blank=True, null=True)),
                ('fromStaff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='accounts.profile')),
                ('holiday', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.holidays')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.projects')),
                ('staff', models.ManyToManyField(blank=True, to='accounts.profile')),
            ],
            options={
                'db_table': 'alerts',
            },
        ),
    ]
