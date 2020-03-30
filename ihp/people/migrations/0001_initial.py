# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-03-04 16:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import geonode.people.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('people', '0027_auto_20200213_1515'),
    ]

    operations = [
        migrations.CreateModel(
            name='IHPProfile',
            fields=[
                ('profile_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='people.Profile')),
                ('approved', models.BooleanField(default=False, help_text='approve user', verbose_name='Is the user approved?')),
                ('recommendation', models.CharField(blank=True, default=b'', help_text='Name of the person who recommended you IHP-WINS', max_length=50, null=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('people.profile',),
            managers=[
                ('objects', geonode.people.models.ProfileUserManager()),
            ],
        ),
    ]
