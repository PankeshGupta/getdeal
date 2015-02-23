# -*- coding: utf-8 -*-
"""
Created on Aug 25, 2013
"""
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule


class UndealSpider(CrawlSpider):
    name = 'undeal'
    allowed_domains = ['undeal.ma']
    start_urls = ['http://www.undeal.ma/']

    rules = (
        Rule(SgmlLinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        pass
