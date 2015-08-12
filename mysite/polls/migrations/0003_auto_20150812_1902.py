# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_avvblogscraptable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avvblogscraptable',
            name='entry_content_text',
            field=models.TextField(null=True, blank=True),
        ),
    ]
