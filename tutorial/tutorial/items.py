# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DmozItem(scrapy.Item):
    domain_name = scrapy.Field()
    domain_link = scrapy.Field()
    main_title = scrapy.Field()
    main_title_link = scrapy.Field()
    blog_title = scrapy.Field()
    blog_link = scrapy.Field()
    category_title = scrapy.Field()
    category_link = scrapy.Field()
    sub_category_title = scrapy.Field()
    sub_category_link = scrapy.Field()
    entry_content_html = scrapy.Field()
    entry_content_text = scrapy.Field()
    created_on = scrapy.Field()