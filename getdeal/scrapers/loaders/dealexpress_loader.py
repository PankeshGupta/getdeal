# -*- coding: utf-8 -*-
"""
Created on Aug 31, 2013
"""
from scrapy.contrib.loader.processor import MapCompose, Identity
from scrapers.loaders.processors import DealLoaderBase, sanitize_phones


class DealLoader(DealLoaderBase):

    supplier_phones_in = MapCompose(unicode.strip, sanitize_phones)
    supplier_phones_our = Identity()
