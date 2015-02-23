# -*- coding: utf-8 -*-
"""
Created on Aug 25, 2013
"""
import re
import time
from urlparse import urljoin, urlparse
from selenium import webdriver

from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import HtmlXPathSelector

from scrapers.settings import path_to_phatomjs
from scrapers.items import DealItem
from scrapers.loaders.hmizate_loader import DealLoader
from apps.dsites.models import DSite
from apps.addresses.models import CityMapping
from apps.categories.models import CategoryMapping


class HmizateSpider(CrawlSpider):
    name = 'hmizate'

    def __init__(self, dsite_pk='', city_mapping_pk='', category_mapping_pk='', updating='False',
                 *args, **kwargs):
        self.dsite = DSite.objects.get(pk=int(dsite_pk)) if dsite_pk else DSite.objects.get(name=self.name)
        self.allowed_domains = [urlparse(self.dsite.url).netloc]
        self.city_mapping = CityMapping.objects.get(pk=city_mapping_pk) if city_mapping_pk else None
        self.category_mapping = CategoryMapping.objects.get(pk=category_mapping_pk) if category_mapping_pk else None
        self.updating = eval(updating)
        self.driver = webdriver.PhantomJS(path_to_phatomjs)
        if self.city_mapping is not None:
            self.start_url = '/deal/%s.html' % self.city_mapping.site_city
        elif self.category_mapping is not None:
            self.start_url = '/deal/%s.html' % self.category_mapping.site_category
        self.deal_urls = ''
        self.item_fields = {'title': ['//div[@class="topcontent clearfix"]/h1/span/text()'],
                            'description1': ['//div[@class="bottom_description"]/span/ul[1]/li/text()'],
                            'description2': ['//*[@id="review-1"]/div/div[1]/div/p/text()'],
                            'hours': ['//span[@id="cntdwn"]/span[@class="hour"]/b'],
                            'minutes': ['//span[@id="cntdwn"]/span[@class="min"]/b[1]'],
                            'initial_price': [
                                '//div[@class="dicount-boxes"]/div[@class="clsdiscount_prices"][2]/span/text()'],
                            'sell_price': ['//a[@id="scriptbuynow"]/div[@class="price_value"]/text()'],
                            'discount': [
                                '//div[@class="dicount-boxes"]/div[@class="clsdiscount_prices"][3]/span/text()'],
                            'saving': ['//div[@class="dicount-boxes"]/div[@class="clsdiscount_prices"][1]/span/text()'],
                            'nbr_buyers': ['//div[@class="dealstatus"]/div[@class="totalcount"]/span/text()'],
                            'supplier_name': [
                                '//*[@id="review-1"]/div/div/div[@class="company-details"]/address/strong/text()'],
                            'supplier_address': [
                                '//*[@id="review-1"]/div/div/div[@class="company-details"]/address/text()'],
                            'validity': [
                                '//div[@class="bottom_description"]/span/ul[1]/li/*/*/*/text()',
                                '//div[@class="bottom_description"]/span/ul[1]/li/*/*/text()',
                                '//div[@class="bottom_description"]/span/ul[1]/li/*/text()'],
                            'image_urls': ['//img[1][@width="440"]/@src']}
        super(HmizateSpider, self).__init__(*args, **kwargs)

    def quit_driver(self):
        self.driver.quit()

    def start_requests(self):
        yield Request(url=urljoin(self.dsite.url, self.start_url),
                      callback=self.redirect_pages)

    def redirect_pages(self, response):
        yield Request(url='http://www.hmizate.ma/tous-les-deals.html',
                      callback=self.list_deals)

    def list_deals(self, response):
        hxs = HtmlXPathSelector(response)
        reg = re.compile('(?P<category>[^\(]+)\(\d*\)')
        categories = [reg.match(category).group('category') for category in
                      hxs.select('//div[@class="categories"]/ul/li/a/cite/text()').extract() if category != '']
        categories_divs = hxs.select('//div[@class="right_column clearfix"]/div')
        categories_urls = {}
        for ind, category_div in enumerate(categories_divs):
            for category_url in category_div.select('.//div[@class="clsallbox"]/div/div/div[1]/a/@href').extract():
                categories_urls[category_url] = categories[ind]
        for url, category in categories_urls.iteritems():
            yield Request(url=url,
                          meta={'category': category},
                          callback=self.parse_deal)

    def parse_deal(self, response):
        deal_loader = DealLoader(item=DealItem(), response=response)
        #add url value
        deal_loader.add_value('url', u'%s' % response.url)
        # iterate over fields and add xpaths to the loader
        for field, xpaths in self.item_fields.iteritems():
            [deal_loader.add_xpath(field, xpath) for xpath in xpaths]
            #load phantomjs
        self.driver.get(response.url)
        time.sleep(3)
        #add minutes and hours using phantomjs
        deal_loader.add_value('minutes',
                              self.driver.find_element_by_xpath(self.item_fields['minutes']).text)
        deal_loader.add_value('hours',
                              self.driver.find_element_by_xpath(self.item_fields['hours']).text)
        deal_loader.add_value('category', u'%s' % response.meta.get('category', ''))
        yield deal_loader.load_item()
