# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0005_auto_20170911_1202'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='termsofuse',
            name='upload',
        ),
        migrations.AddField(
            model_name='termsofuse',
            name='content_en',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='termsofuse',
            name='content_fr',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='termsofuse',
            name='title_en',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='termsofuse',
            name='title_fr',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
