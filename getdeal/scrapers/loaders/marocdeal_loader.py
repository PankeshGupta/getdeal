# -*- coding: utf-8 -*-
"""
Created on Aug 31, 2013
"""
import re

from scrapy.contrib.loader.processor import MapCompose
from scrapers.loaders.processors import DealLoaderBase, Position, sanitize_phones


def sanitize_supplier(value):
    return value if value else None


def sanitize_time(value):
    reg = re.compile(r'(?P<days>\d+)[a-zA-Z] (?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d+)', re.UNICODE)
    res = reg.match(value)
    if res:
        return [res.group('days'), res.group('hours'), res.group('minutes')]


class DealLoader(DealLoaderBase):
    days_in = MapCompose(unicode.strip, sanitize_time)
    days_out = Position(0)
    hours_in = MapCompose(unicode.strip, sanitize_time)
    hours_out = Position(1)
    minutes_in = MapCompose(unicode.strip, sanitize_time)
    minutes_out = Position(2)
    supplier_name_in = MapCompose(unicode.strip)
    supplier_address_in = MapCompose(unicode.strip, sanitize_supplier)
    supplier_address_out = Position(0)
    supplier_phones_in = MapCompose(unicode.strip, sanitize_phones)
    supplier_phones_out = Position(1)
