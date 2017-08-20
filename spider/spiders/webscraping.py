# -*- coding: utf-8 -*-

from scrapy import Request
from scrapy import Spider

from spider.items import SpiderItem


class WebscrapingSpider(Spider):
    name = "webscraping"
    start_urls = ["http://example.webscraping.com/"]

    def parse(self, response):
        for path in response.xpath('//a'):
            name = path.xpath('text()').extract()[0]
            href = path.xpath('@href').extract()[0]
            link = response.urljoin(href)
            item = SpiderItem(url=response.url, name=name, link=link)
            yield item
            yield Request(link, callback=self.parse)
