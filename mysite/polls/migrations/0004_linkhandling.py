# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_auto_20150812_1902'),
    ]

    operations = [
        migrations.CreateModel(
            name='LinkHandling',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('domain_name', models.CharField(max_length=70, null=True, blank=True)),
                ('domain_link', models.URLField()),
                ('active', models.BooleanField(default=True)),
            ],
        ),
    ]
