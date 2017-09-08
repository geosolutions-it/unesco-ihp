# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutUsPageContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title_en', models.TextField()),
                ('title_fr', models.TextField()),
                ('content_en', models.TextField()),
                ('content_fr', models.TextField()),
            ],
        ),
    ]
