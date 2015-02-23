# -*- coding: utf-8 -*-
"""
Created on Aug 25, 2013
"""
import re
from urlparse import urljoin, urlparse
from selenium import webdriver

from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule


from scrapers.settings import path_to_phatomjs
from scrapers.items import DealItem
from scrapers.loaders.superdeal_loader import DealLoader
from apps.dsites.models import DSite
from apps.addresses.models import CityMapping
from apps.categories.models import CategoryMapping


class SuperdealSpider(CrawlSpider):
    name = 'superdeal'

    def __init__(self, dsite_pk='', city_mapping_pk='', category_mapping_pk='', updating='False',
                 *args, **kwargs):
        self.dsite = DSite.objects.get(pk=int(dsite_pk)) if dsite_pk else DSite.objects.get(name=self.name)
        self.allowed_domains = [urlparse(self.dsite.url).netloc]
        self.city_mapping = CityMapping.objects.get(pk=city_mapping_pk) if city_mapping_pk else None
        self.category_mapping = CategoryMapping.objects.get(pk=category_mapping_pk) if category_mapping_pk else None
        self.updating = eval(updating)
        self.driver = webdriver.PhantomJS(path_to_phatomjs)
        if self.city_mapping is not None:
            self.start_url = '/%s/%s/' % (self.category_mapping.site_category, self.city_mapping.site_city)
            self.deal_urls = re.compile(
                '/' + self.category_mapping.site_category + '|' + self.city_mapping.site_city + '(?=/[a-zA-Z\s\d_-]+/?)')
        else:
            self.start_url = '/%s/' % self.category_mapping.site_category
            self.deal_urls = re.compile('/' + self.category_mapping.site_category + '(?=/[a-zA-Z\s\d_-]+/?)')
        self.rules = (
            Rule(SgmlLinkExtractor(allow=self.deal_urls, restrict_xpaths='//*[@id="deal_main"]'),
                 callback='parse_deal', follow=False),
            Rule(SgmlLinkExtractor(allow=self.deal_urls, restrict_xpaths='//*[@id="alldeals"]'),
                 callback='parse_deal', follow=False),
        )
        self.item_fields = {'title': '//div[@id="desc"]/h2/a/span/text()',
                            'description1': '//div[@id="offre"]/ul/li/span/text()',
                            'description2': '//div[@id="article"]/p/span/text()',
                            'hours': '//span[@id="remaining-hours"]/text()',
                            'minutes': '//span[@id="remaining-minutes"]/text()',
                            'initial_price': '//span[@class="dd"][1]/span/text()',
                            'sell_price': '//div[@id="deal_price_tag"]/span/text()',
                            'discount': '//span[@class="dd"][2]/span/text()',
                            'saving': '//span[@class="dd"][3]/span/text()',
                            'nbr_buyers': '//div[@id="deal_status"]/p/text()',
                            'supplier_name': '//div[@id="left-smt"]/div/div/h3/text()',
                            'supplier_address': '//div[@id="left-smt"]/div/div/div[2]/@onclick',
                            'supplier_lat': '//div[@id="left-smt"]/div/div/div[2]/@onclick',
                            'supplier_lng': '//div[@id="left-smt"]/div/div/div[2]/@onclick',
                            'supplier_city': '//div[@id="left-smt"]/div/div/div[2]/@onclick',
                            'supplier_phones': '//div[@id="left-smt"]/div/div/div[2]/@onclick',
                            'image_urls': '//div[@id="banners"]/div/img[1]/@src'}
        super(SuperdealSpider, self).__init__(*args, **kwargs)

    def quit_driver(self):
        self.driver.quit()

    def start_requests(self):
        yield Request(url=urljoin(self.dsite.url, self.start_url))

    def parse_deal(self, response):
        deal_loader = DealLoader(item=DealItem(), response=response)
        #add url value
        deal_loader.add_value('url', u'%s' % response.url)

        # iterate over fields and add xpaths to the loader
        for field, xpath in self.item_fields.iteritems():
            deal_loader.add_xpath(field, xpath)

        deal_loader.add_xpath('validity', '//div[@id="conditions"]/ul/li[1]/span/text()')
        deal_loader.add_xpath('validity', '//div[@id="conditions"]/div/ul/li[1]/span/text()')

        yield deal_loader.load_item()
