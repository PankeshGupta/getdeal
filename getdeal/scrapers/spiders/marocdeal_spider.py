# -*- coding: utf-8 -*-
"""
Created on Aug 25, 2013
"""
import time
from urlparse import urljoin, urlparse
from selenium import webdriver

from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import HtmlXPathSelector

from scrapers.settings import path_to_phatomjs
from scrapers.items import DealItem
from scrapers.loaders.marocdeal_loader import DealLoader
from apps.dsites.models import DSite
from apps.addresses.models import CityMapping
from apps.categories.models import CategoryMapping


class MarocdealSpider(CrawlSpider):
    name = 'marocdeal'

    def __init__(self, dsite_pk='', city_mapping_pk='', category_mapping_pk='', updating='False',
                 *args, **kwargs):
        self.dsite = DSite.objects.get(pk=int(dsite_pk)) if dsite_pk else DSite.objects.get(name=self.name)
        self.allowed_domains = [urlparse(self.dsite.url).netloc]
        self.city_mapping = CityMapping.objects.get(pk=city_mapping_pk) if city_mapping_pk else None
        self.category_mapping = CategoryMapping.objects.get(pk=category_mapping_pk) if category_mapping_pk else None
        self.updating = eval(updating)
        self.driver = webdriver.PhantomJS(path_to_phatomjs)
        self.start_url = '/deal-categories/%s/?deals=%s' % (
            self.category_mapping.site_category, self.city_mapping.site_city if self.city_mapping else 'casablanca')
        self.deal_urls = ''
        self.item_fields = {'title': '//div[@class="tile-deal"]/h1[@class="tile-title-deal"]/text()',
                            'description1': '//div[@id="deal_details"]/div[1]/div/ul/li/text()',
                            #'description2': '//div[@id="article"]/p/span/text()',
                            'days': '//span[@class="countdown_row countdown_amount"]',
                            'hours': '//span[@class="countdown_row countdown_amount"]',
                            'minutes': '//span[@class="countdown_row countdown_amount"]',
                            'initial_price': '//li[@class="worth"]/span[2]/text()',
                            'sell_price': '//li[@class="price"]/span[2]/text()',
                            'discount': '//span[@class="deal-savings"]/text()',
                            'nbr_buyers': '//div[@class="sold-deal"]/text()',
                            'supplier_name': '//div[@id="merchant-name"]/text()',
                            'supplier_address': '//div[@id="merchant-info"]/text()',
                            #'supplier_lat': '//a[@class="modal_map"]/img/@src',
                            #'supplier_lng': '//a[@class="modal_map"]/img/@src',
                            'supplier_phones': '//div[@id="merchant-info"]/text()',
                            'validity': '//div[2]/div[@class="deal_how_to"]/ul/li[3]/text()',
                            'image_urls': '//div[@id="portfolio-slideshow0"]/div[1]/a/img/@src'}
        super(MarocdealSpider, self).__init__(*args, **kwargs)

    def quit_driver(self):
        self.driver.quit()

    def start_requests(self):
        yield Request(url=urljoin(self.dsite.url, self.start_url),
                      callback=self.list_deals)

    def list_deals(self, response):
        hxs = HtmlXPathSelector(response)
        for deal_wrapper in hxs.select('//div[@class="wrapper"]'):
            if not deal_wrapper.select('.//img[@class="expired"]').extract():
                deal_url = deal_wrapper.select('.//a[@class="buy-button index"]/@href').extract()[0]
                yield Request(url=deal_url, callback=self.parse_deal)

    def parse_deal(self, response):
        deal_loader = DealLoader(item=DealItem(), response=response)
        #add url value
        deal_loader.add_value('url', u'%s' % response.url)

        # iterate over fields and add xpaths to the loader
        for field, xpath in self.item_fields.iteritems():
            deal_loader.add_xpath(field, xpath)
        #load phantomjs
        self.driver.get(response.url)
        time.sleep(3)
        #add minutes and hours using phantomjs
        deal_loader.add_value('minutes',
                              self.driver.find_element_by_xpath(self.item_fields['minutes']).text)
        deal_loader.add_value('hours',
                              self.driver.find_element_by_xpath(self.item_fields['hours']).text)
        deal_loader.add_value('days',
                              self.driver.find_element_by_xpath(self.item_fields['days']).text)
        deal_loader.add_value('supplier_city', u'%s' %
                                               self.city_mapping.target_city if self.city_mapping else u'')
        yield deal_loader.load_item()
