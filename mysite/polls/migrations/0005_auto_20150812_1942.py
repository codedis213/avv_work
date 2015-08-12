# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_linkhandling'),
    ]

    operations = [
        migrations.AddField(
            model_name='linkhandling',
            name='changed_on',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 12, 19, 41, 29, 893961), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='linkhandling',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 12, 19, 42, 1, 956901, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
