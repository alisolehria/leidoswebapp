# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-27 12:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20161227_0137'),
    ]

    operations = [
        migrations.CreateModel(
            name='projectsWithSkills',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('projectID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.projects')),
            ],
            options={
                'db_table': 'projectsWithSkills',
            },
        ),
        migrations.CreateModel(
            name='skills',
            fields=[
                ('skillID', models.AutoField(primary_key=True, serialize=False)),
                ('skillName', models.CharField(max_length=200)),
                ('projectID', models.ManyToManyField(through='accounts.projectsWithSkills', to='accounts.projects')),
            ],
            options={
                'db_table': 'skills',
            },
        ),
        migrations.CreateModel(
            name='staffWithSkills',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skillID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.skills')),
                ('staffID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.profile')),
            ],
            options={
                'db_table': 'staffWithSkills',
            },
        ),
        migrations.AddField(
            model_name='skills',
            name='staffID',
            field=models.ManyToManyField(through='accounts.staffWithSkills', to='accounts.profile'),
        ),
        migrations.AddField(
            model_name='projectswithskills',
            name='skillID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.skills'),
        ),
    ]