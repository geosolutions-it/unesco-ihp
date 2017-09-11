# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0004_contactuspagecontent'),
    ]

    operations = [
        migrations.CreateModel(
            name='FaqQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title_en', models.TextField()),
                ('title_fr', models.TextField()),
                ('content_en', models.TextField()),
                ('content_fr', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='FaqTopic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title_en', models.TextField()),
                ('title_fr', models.TextField()),
                ('order', models.PositiveIntegerField()),
                ('questions', models.ManyToManyField(to='content.FaqQuestion', blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='faqquestion',
            name='topic',
            field=models.ForeignKey(to='content.FaqTopic'),
        ),
    ]
