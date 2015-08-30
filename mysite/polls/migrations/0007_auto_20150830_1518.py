# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_emailhandling'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='emailhandling',
            table='avv_blog_email_handling_table',
        ),
    ]
