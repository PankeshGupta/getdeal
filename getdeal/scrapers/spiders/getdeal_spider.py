# -*- coding: utf-8 -*-
"""
Created on Sep 21, 2013
"""
from urlparse import urlparse
from selenium import webdriver

from scrapy.contrib.spiders import CrawlSpider

from scrapers.settings import path_to_phatomjs
from apps.dsites.models import DSite
from apps.addresses.models import CityMapping
from apps.categories.models import CategoryMapping


class GetdealSpider(CrawlSpider):
    def __init__(self, *args, **kwargs):
        dsite_pk = kwargs.get('dsite_pk', '')
        if dsite_pk:
            self.dsite = DSite.objects.get(pk=dsite_pk)
        else:
            self.dsite = DSite.objects.get(name=self.name)
        self.allowed_domains = [urlparse(self.dsite.url).netloc]
        city_mapping_pk = kwargs.get('city_mapping_pk', '')
        if city_mapping_pk:
            self.city_mapping = CityMapping.objects.get(pk=city_mapping_pk)
        else:
            self.city_mapping = None
        category_mapping_pk = kwargs.get('category_mapping_pk', '')
        if category_mapping_pk:
            self.category_mapping = CategoryMapping.objects.get(pk=category_mapping_pk)
        else:
            self.category_mapping = None
        self.updating = kwargs.get('updating', False)
        self.driver = webdriver.PhantomJS(path_to_phatomjs)
        self.start_url = ''
        self.deal_urls = ''
        self.item_fields = {}
        super(GetdealSpider, self).__init__(*args, **kwargs)

    def __del__(self):
        self.driver.quit()
        del self
