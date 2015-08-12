# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AvvBlogScrapTable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('domain_name', models.CharField(max_length=70)),
                ('domain_link', models.URLField()),
                ('main_title', models.CharField(max_length=70)),
                ('main_title_link', models.URLField()),
                ('blog_title', models.CharField(max_length=70)),
                ('blog_link', models.URLField()),
                ('category_title', models.CharField(max_length=70, null=True)),
                ('category_link', models.URLField(null=True)),
                ('sub_category_title', models.CharField(max_length=70, null=True, blank=True)),
                ('sub_category_link', models.URLField(null=True, blank=True)),
                ('entry_content_html', models.TextField()),
                ('entry_content_text', models.TextField(null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('changed_on', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'avv_blog_scrap_table',
            },
        ),
    ]
