# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_aboutuspagecontent'),
    ]

    operations = [
        migrations.CreateModel(
            name='PartnerIcon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('upload', models.FileField(upload_to=b'partner-ico')),
                ('name', models.CharField(max_length=255)),
                ('href', models.TextField()),
            ],
        ),
    ]
