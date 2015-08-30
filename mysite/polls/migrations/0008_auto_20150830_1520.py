# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_auto_20150830_1518'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='linkhandling',
            table='avv_blog_link_handling_table',
        ),
    ]
