# -*- coding: utf-8 -*-
"""
Created on Aug 31, 2013
"""
import re

from scrapy.contrib.loader.processor import MapCompose, Identity
from scrapers.loaders.processors import DealLoaderBase, Position, sanitize_phones, sanitize_coordinates


def sanitize_address(value):
    if not re.findall('Tel', value):
        return value


class DealLoader(DealLoaderBase):

    supplier_address_in = MapCompose(unicode.strip, sanitize_address)
    supplier_phones_in = MapCompose(unicode.strip, sanitize_phones)
    supplier_phones_out = Identity()
    supplier_lat_in = MapCompose(unicode.strip, sanitize_coordinates)
    supplier_lat_out = Position(0)
    supplier_lng_in = MapCompose(unicode.strip, sanitize_coordinates)
    supplier_lng_out = Position(1)
    #@todo : clean description
    #@todo : clean phones
