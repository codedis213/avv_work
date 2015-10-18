import scrapy

from tutorial.items import DmozItem
from scrapy.selector import Selector


class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["stackoverflow.com"]
    start_urls = [
        "http://stackoverflow.com/questions?pagesize=50&sort=newest",
    ]

    def parse(self, response):
        questions = Selector(response).xpath('//div[@class="summary"]/h3')

        for question in questions:
            item = DmozItem()
            item['title'] = question.xpath(
                'a[@class="question-hyperlink"]/text()').extract()[0]
            item['link'] = question.xpath(
                'a[@class="question-hyperlink"]/@href').extract()[0]
            item['des'] = question.xpath(
                'a[@class="question-hyperlink"]/@href').extract()[0]

            return item

