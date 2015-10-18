# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log
import MySQLdb


class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoDBPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert(dict(item))
            log.msg("Question added to MongoDB database!",
                    level=log.DEBUG, spider=spider)
        return item


class AmazoncrawlerPipeline(object):
    host = 'localhost'
    user = 'root'
    password = 'root'
    db = 'avv_blog_scrap'

    def __init__(self):
        self.connection = MySQLdb.connect(self.host, self.user, self.password, self.db)
        self.cursor = self.connection.cursor()
        self.connection.set_character_set('utf8')
        self.cursor.execute('SET NAMES utf8;')
        self.cursor.execute('SET CHARACTER SET utf8;')
        self.cursor.execute('SET character_set_connection=utf8;')

    def process_item(self, item, spider):
        try:
            sql = """INSERT INTO avv_blog_scrap_table
                (domain_name, domain_link, main_title, main_title_link,
                blog_title, blog_link, category_title, category_link,
                sub_category_title, sub_category_link,
                entry_content_html, entry_content_text, created_on)
                VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"""


            self.cursor.execute(sql, (item['domain_name'], item['domain_link'], item['main_title'],
                                      item['main_title_link'], item['blog_title'], item['blog_link'],
                                      item['category_title'], item['category_link'], item['sub_category_title'],
                                      item['sub_category_link'], item['entry_content_html'], item['entry_content_text'],
                                      item['created_on']))

            self.connection.commit()

        except MySQLdb.Error, e:
            print 'Error %d: %s' % (e.args[0], e.args[1])

        return item


