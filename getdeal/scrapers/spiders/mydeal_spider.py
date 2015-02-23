# -*- coding: utf-8 -*-
"""
Created on Aug 25, 2013
"""
import re
import time
from urlparse import urljoin, urlparse
from selenium import webdriver

from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule

from scrapers.settings import path_to_phatomjs
from scrapers.items import DealItem
from scrapers.loaders.mydeal_loader import DealLoader
from apps.dsites.models import DSite
from apps.addresses.models import CityMapping
from apps.categories.models import CategoryMapping


class MydealSpider(CrawlSpider):
    name = 'mydeal'

    def __init__(self, dsite_pk='', city_mapping_pk='', category_mapping_pk='', updating='False',
                 *args, **kwargs):
        self.dsite = DSite.objects.get(pk=int(dsite_pk)) if dsite_pk else DSite.objects.get(name=self.name)
        self.allowed_domains = [urlparse(self.dsite.url).netloc]
        self.city_mapping = CityMapping.objects.get(pk=city_mapping_pk) if city_mapping_pk else None
        self.category_mapping = CategoryMapping.objects.get(pk=category_mapping_pk) if category_mapping_pk else None
        self.updating = eval(updating)
        self.driver = webdriver.PhantomJS(path_to_phatomjs)
        if self.city_mapping is not None:
            self.deal_urls = re.compile('/' + self.city_mapping.site_city + '/[a-zA-Z\d_-]+.html')
            self.start_url = "/%s/deal/%s.htm" % (self.city_mapping.site_city, self.category_mapping.site_category)
        else:
            self.deal_urls = re.compile('/[a-zA-Z\d]+' + '/[a-zA-Z\d_-]+.html')
            self.start_url = "/deal/%s.html" % self.category_mapping.site_category
        self.rules = (Rule(SgmlLinkExtractor(allow=self.deal_urls, restrict_xpaths=(
            '//*[@id="div_current_deals"]', '//*[@id="wrap_slider"]', '//*[@class="slider-wrapper"]')),
            callback='parse_deal', follow=False),
        )
        self.item_fields = {'title': '//div[@id="title_deal_of_day"]/text()',
                            #@todo : add descriptions
                            'description1': '//*[@id="conditions"]/ul/li/text()',
                            'description2': '//*[@id="description_deal"]/*',
                            'days': '//div[@class="jours"]/div[1]',
                            'hours': '//div[@class="heures"]/div[1]',
                            'minutes': '//div[@class="min"]/div[1]',
                            'initial_price': '//span[@class="prix_remise"]/text()',
                            'sell_price': '//div[ @class="prix"]/text()',
                            'discount': '//span[@class="remise"]/text()',
                            #'saving': '',
                            'nbr_buyers': '//div[@class="title_partic"]/span/text()',
                            'supplier_name': '//div[@id="div_enseigne_title"]/strong/text()',
                            'supplier_address': '//div[@id="enseigne"]/ul/li/text()',
                            'supplier_lat': '//a[@class="modal_map"]/img/@src',
                            'supplier_lng': '//a[@class="modal_map"]/img/@src',
                            #'supplier_city': '',
                            #'supplier_phones': '',
                            'validity': '//div[@id="conditions"]/ul/li[1]/text()',
                            'image_urls': '//div[@id="slider"]/img[1]/@src'}
        super(MydealSpider, self).__init__(*args, **kwargs)

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
        yield deal_loader.load_item()
