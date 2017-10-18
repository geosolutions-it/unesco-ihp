# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0006_auto_20171006_1856'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentationPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('title_en', models.TextField()),
                ('title_fr', models.TextField()),
                ('order', models.PositiveIntegerField()),
                ('content_en', models.TextField()),
                ('content_fr', models.TextField()),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', blank=True, to='content.DocumentationPage', null=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name_plural': 'Documentation',
            },
        ),
    ]
