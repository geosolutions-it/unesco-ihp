# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0007_documentationpage'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='documentationpage',
            options={'ordering': ('order',), 'verbose_name_plural': 'Documentation'},
        ),
    ]
