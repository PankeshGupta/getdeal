# -*- coding: utf-8 -*-
"""
Created on Aug 25, 2013
"""
import time
from urlparse import urlparse
from selenium import webdriver

from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider

from scrapers.settings import path_to_phatomjs
from scrapers.items import DealItem
from scrapers.loaders.processors import DealLoaderBase as DealLoader
from apps.dsites.models import DSite
from apps.addresses.models import CityMapping
from apps.categories.models import CategoryMapping


class GrouponSpider(CrawlSpider):
    name = 'groupon'

    def __init__(self, dsite_pk='', city_mapping_pk='', category_mapping_pk='', updating='False',
                 *args, **kwargs):
        self.dsite = DSite.objects.get(pk=int(dsite_pk)) if dsite_pk else DSite.objects.get(name=self.name)
        self.allowed_domains = [urlparse(self.dsite.url).netloc]
        self.city_mapping = CityMapping.objects.get(pk=city_mapping_pk) if city_mapping_pk else None
        self.category_mapping = CategoryMapping.objects.get(pk=category_mapping_pk) if category_mapping_pk else None
        self.updating = eval(updating)
        self.driver = webdriver.PhantomJS(path_to_phatomjs)
        self.start_url = ''
        self.deal_urls = ''
        self.item_fields = {'title': '//div[@id="deal_shorttitle"]/h2/text()',
                            'description1': '//div[@class="box_content deal_description"]/p[1]/span/text()',
                            #'description2': '//div[@id="article"]/p/span/text()',
                            'hours': '//div[@id="deal_title"]/div[4]/text()',
                            #'minutes': '//span[@id="cntdwn"]/span[@class="min"]/b[1]',
                            'initial_price': '//div[@class="box_deal_price"]/span[2]/text()',
                            'sell_price': '//div[@class="box_deal_price"]/span[1]/text()',
                            'discount': '//div[@id="deal_title"]/div[2]/text()',
                            'saving': '//div[@class="dicount-boxes"]/div[@class="clsdiscount_prices"][1]/span/text()',
                            #'nbr_buyers': '//div[@class="dealstatus"]/div[@class="totalcount"]/span/text()',
                            'supplier_name': '//div[@id="deal_title"]/div[1]/text()',
                            'supplier_address': '//*[@id="review-1"]/div/div/div[@class="company-details"]/address/text()',
                            'validity': '//p[@class="valable"]/text()',
                            'image_urls': '//div[@class="fwrap"]/ul/li[1]/img/@src'}
        super(GrouponSpider, self).__init__(*args, **kwargs)

    def quit_driver(self):
        self.driver.quit()

    def start_requests(self):
        #load phantomjs
        self.driver.get('%s/%s' % (self.dsite.url, self.category))
        time.sleep(3)
        for deal_url in self.driver.find_elements_by_xpath('//div[@class="product dealsbox_content"]/div/a'):
            yield Request(url=deal_url.get_attribute('href'),
                          callback=self.parse_deal)

    def parse_deal(self, response):
        deal_loader = DealLoader(item=DealItem(), response=response)
        #add url value
        deal_loader.add_value('url', u'%s' % response.url)
        # iterate over fields and add xpaths to the loader
        for field, xpath in self.item_fields.iteritems():
            deal_loader.add_xpath(field, xpath)

        deal_loader.add_value('category', u'%s' % self.category)
        print deal_loader.load_item()
        yield ""
