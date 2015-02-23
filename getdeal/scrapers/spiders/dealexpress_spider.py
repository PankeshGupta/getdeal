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
from scrapers.loaders.dealexpress_loader import DealLoader
from apps.dsites.models import DSite
from apps.addresses.models import CityMapping
from apps.categories.models import CategoryMapping


class DealexpressSpider(CrawlSpider):
    name = 'dealexpress'

    def __init__(self, dsite_pk='', city_mapping_pk='', category_mapping_pk='', updating='False',
                 *args, **kwargs):
        self.dsite = DSite.objects.get(pk=int(dsite_pk)) if dsite_pk else DSite.objects.get(name=self.name)
        self.allowed_domains = [urlparse(self.dsite.url).netloc]
        self.city_mapping = CityMapping.objects.get(pk=city_mapping_pk) if city_mapping_pk else None
        self.category_mapping = CategoryMapping.objects.get(pk=category_mapping_pk) if category_mapping_pk else None
        self.updating = eval(updating)
        self.driver = webdriver.PhantomJS(path_to_phatomjs)
        self.start_url = '/dealexpress-ville-%s-theme.html' % self.city_mapping.site_city
        self.deal_urls = ''
        self.item_fields = {'title': '//div[@id="content"]/div[3]/text()',
                            'description1': '//div[@id="garanties"]/div[1]/div[2]/ol/li/text()',
                            'description2': '//div[@id="garanties"]/text()',
                            'hours': '//label[@id="comptee"]',
                            'minutes': '//label[@id="compto"]',
                            'initial_price': '//div[@id="detailachat"]/table/tbody/tr[2]/td[1]',
                            'sell_price': '//div[@id="prixforme"]/span/text()',
                            'discount': '//div[@id="detailachat"]/table/tbody/tr[2]/td[2]',
                            'saving': '//div[@id="detailachat"]/table/tbody/tr[2]/td[3]',
                            'nbr_buyers': '//div[@id="searchBox"]/div[5]/text()',
                            'supplier_address': '//div[@id="ad"]/div[1]/span/text()',
                            'supplier_phones': '//div[@id="garanties"]/div[2]/div[2]/ol/li/text()',
                            'validity': '//div[@id="garanties"]/div[2]/div[2]/ol/li[1]/text()',
                            'image_urls': '//div[@id="bannerHolder"]/a[1]/img/@src'}
        super(DealexpressSpider, self).__init__(*args, **kwargs)

    def quit_driver(self):
        self.driver.quit()

    def start_requests(self):
        yield Request(url=urljoin(self.dsite.url, self.start_url),
                      callback=self.list_deals)

    def list_deals(self, response):
        hxs = HtmlXPathSelector(response)
        meta = {}
        for deal_wrapper in hxs.select('//div[@id="iid"]/div/div/div'):
            deal_url = urljoin(self.dsite.url, deal_wrapper.select('.//div[2]/div/div[2]/span/a/@href').extract()[0])
            meta['category'] = deal_wrapper.select('.//div[2]/div/div[1]/a/span/b/text()').extract()[0]
            meta['supplier_name'] = deal_wrapper.select('.//div[2]/div/a/h3/text()').extract()[0]
            yield Request(url=deal_url, meta=meta, callback=self.parse_deal)

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
        #add minutes, hours, prices and discount using phantomjs
        deal_loader.add_value('minutes',
                              self.driver.find_element_by_xpath(self.item_fields['minutes']).text)
        deal_loader.add_value('hours',
                              self.driver.find_element_by_xpath(self.item_fields['hours']).text)
        deal_loader.add_value('initial_price',
                              self.driver.find_element_by_xpath(self.item_fields['initial_price']).text)
        deal_loader.add_value('discount',
                              self.driver.find_element_by_xpath(self.item_fields['discount']).text)
        deal_loader.add_value('saving',
                              self.driver.find_element_by_xpath(self.item_fields['saving']).text)
        deal_loader.add_value('category', u'%s' % response.meta['category'])
        deal_loader.add_value('supplier_name', u'%s' % response.meta['supplier_name'])
        yield deal_loader.load_item()
