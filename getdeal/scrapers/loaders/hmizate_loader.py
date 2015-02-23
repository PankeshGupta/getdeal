# -*- coding: utf-8 -*-
"""
Created on Aug 31, 2013
"""
from scrapy.contrib.loader.processor import MapCompose
from scrapers.loaders.processors import DealLoaderBase


class DealLoader(DealLoaderBase):
    supplier_name_in = MapCompose(unicode.strip)
    supplier_address_in = MapCompose(unicode.strip)
