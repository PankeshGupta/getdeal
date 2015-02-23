# -*- coding: utf-8 -*-
"""
Created on Aug 31, 2013
"""
from scrapy.contrib.loader.processor import MapCompose
from scrapers.loaders.processors import DealLoaderBase, Position, sanitize_coordinates


class DealLoader(DealLoaderBase):
    supplier_name_in = MapCompose(unicode.strip)
    supplier_address_in = MapCompose(unicode.strip)
    supplier_lat_in = MapCompose(unicode.strip, sanitize_coordinates)
    supplier_lat_out = Position(0)
    supplier_lng_in = MapCompose(unicode.strip, sanitize_coordinates)
    supplier_lng_out = Position(1)
