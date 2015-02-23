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
from scrapers.loaders.dealin_loader import DealLoader
from apps.dsites.models import DSite
from apps.addresses.models import CityMapping
from apps.categories.models import CategoryMapping


class DealinSpider(CrawlSpider):
    name = 'dealin'

    def __init__(self, dsite_pk='', city_mapping_pk='', category_mapping_pk='', updating='False',
                 *args, **kwargs):
        self.dsite = DSite.objects.get(pk=int(dsite_pk)) if dsite_pk else DSite.objects.get(name=self.name)
        self.allowed_domains = [urlparse(self.dsite.url).netloc]
        self.city_mapping = CityMapping.objects.get(pk=city_mapping_pk) if city_mapping_pk else None
        self.category_mapping = CategoryMapping.objects.get(pk=category_mapping_pk) if category_mapping_pk else None
        self.updating = eval(updating)
        self.driver = webdriver.PhantomJS(path_to_phatomjs)
        self.start_url = '%s' % self.category_mapping.site_category
        self.deal_urls = ''
        self.item_fields = {'title': '//div[@id="deal625x398-wrapper"]/ul/li[@class="dealTitle"]/a/text()',
                            'description1': '//ul[@class="unIndentedList"]/li/span/span/text()',
                            'description2': '//*[@id="dealDetail"]/div[3]/div[2]/div[3]/div/p/span/span/text()',
                            'days': '//div[@id="deal_days_rem"]',
                            'hours': '//div[@id="deal_hours_rem"]',
                            'minutes': '//div[@id="deal_minutes_rem"]',
                            'initial_price': '//div[@id="metaStrip"]/ul/li[1]/span/text()',
                            'sell_price': '//div[@id="topLeft"]/div/div/div/div[@class="pbdiv"]/div[@class="pbdivprc"]/p/text()',
                            'saving': '//a[@id="deal_main_map_link"]/text()',
                            'discount': '//div[@id="metaStrip"]/ul/li[2]/span/text()',
                            'nbr_buyers': '//*[@id="dpb_143143_sold"]/text()',
                            'supplier_name': '//div[@class="merchInfo"]/p[1]/span/span/strong/span/text()',
                            'supplier_address': '//div[@class="merchInfo"]/p/span/span/text()',
                            'supplier_city': '//div[@class="merchInfo"]/p/span/span/text()',
                            'supplier_phones': '//div[@class="merchInfo"]/p/span/span/text()',
                            'supplier_lat': '//div[@id="dealDetail"]/div[3]/div[1]/div[3]/div/div/a/@href',
                            'supplier_lng': '//div[@id="dealDetail"]/div[3]/div[1]/div[3]/div/div/a/@href',
                            'validity': 'div[@class="blockContent"]/ul/li[1]/span/span/text()',
                            'image_urls': '//div[@class="photoInner"]/img[1]/@src'}
        super(DealinSpider, self).__init__(*args, **kwargs)

    def quit_driver(self):
        self.driver.quit()

    def start_requests(self):
        yield Request(url=urljoin(self.dsite.url, self.start_url),
                      callback=self.list_deals)

    def list_deals(self, response):
        hxs = HtmlXPathSelector(response)
        for deal_url in hxs.select('//div[@class="bottomColumn1"]/div/div/div[2]/div[2]/div/a/@href'):
            deal_url = urljoin(self.dsite.url, deal_url.extract())
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
        #add days, minutes, hours using phantomjs
        deal_loader.add_value('minutes',
                              self.driver.find_element_by_xpath(self.item_fields['minutes']).text)
        deal_loader.add_value('hours',
                              self.driver.find_element_by_xpath(self.item_fields['hours']).text)
        deal_loader.add_value('days',
                              self.driver.find_element_by_xpath(self.item_fields['days']).text)
        yield deal_loader.load_item()
