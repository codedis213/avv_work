# -*- coding: utf-8 -*-
import scrapy

from tutorial.items import DmozItem
from scrapy.selector import Selector
from bs4 import BeautifulSoup
import re
import datetime

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["www.highya.com"]
    start_urls = [
        "http://www.highya.com/",
    ]

    def parse(self, response):
        soup = BeautifulSoup(response.body, "html.parser")

        ul_box = soup.find("ul", {"class":"no-list list-related list-articles clearfix"})
        li_list = ul_box.find_all("li")

        for li in li_list:
            url = li.find("a", {"class":"a-st2"}).get("href")
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        # try:
            item = DmozItem()
            soup2 = BeautifulSoup(response.body, "html.parser")
            item["domain_name"] = "highya.com"
            item["domain_link"] = "http://www.highya.com/"
            article_div = soup2.find("article", {"class":"product-article"})
            item["main_title"] = article_div.find("h1").get_text()
            item["main_title_link"] = response.url
            item["blog_title"] = item["main_title"]
            item["blog_link"] = item["main_title_link"]
            option_div = article_div.find("div", {"class":"options ind-p"})
            category_a = option_div.find("li", text=re.compile('Category')).find_parent("ul").find("a")
            item["category_title"] = category_a.get_text()
            item["category_link"] = category_a.get("href")
            item["sub_category_title"] = ''
            item["sub_category_link"] = ''
            section_article = soup2.find("div", {"class":"site-section section-article"})
            item["entry_content_html"] = str(section_article.encode("ascii", "ignore"))
            item["entry_content_text"] = section_article.get_text()
            item["created_on"] = datetime.datetime.now()

            yield  item
        # except:
        #     pass



