# -*- coding: utf-8 -*-
"""
Created on Aug 31, 2013
"""
import re

from scrapy.contrib.loader.processor import MapCompose
from scrapers.loaders.processors import DealLoaderBase, Position


def sanitize_supplier(value):
    digit_content = u'[\d\.-]+'
    content = u'[^\"]+'
    separators = u'[,\s]*'
    quotes = u'\"?'
    reg = re.compile(r'showMap\(' +
                     quotes + '(?P<lat>' + digit_content + ')' + quotes + separators +
                     quotes + '(?P<lng>' + digit_content + ')' + quotes + separators +
                     quotes + '(?P<supplier_name>' + content + ')' + quotes + separators +
                     quotes + '(?P<supplier_address>' + content + ')' + quotes + separators +
                     quotes + '(?P<supplier_phones>' + content + ')' + quotes + separators +
                     quotes + '(?P<supplier_city>' + content + ').*\)', re.UNICODE)
    #reg = re.compile(ur'showMap\((?P<lat>[\d\.]+)[,\s\"]*(?P<lng>[\d\.-]+)[,\s\"]*(?P<supplier_name>[éèêâôûîàùç–´’°&\s\d\w\(\)\.\',_-]+)[,\s\"]*(?P<supplier_address>[éèêâôûîàùç–´’°&\s\d\w\(\)\.\',_-]+)[,\s\"]*(?P<supplier_phones>[\d\s-]+)[,\s\"]*(?P<supplier_city>[\w]+).*\)', re.UNICODE)
    res = reg.match(value)
    if res:
        return [res.group('lat'), res.group('lng'), res.group('supplier_name'), res.group('supplier_address'),
                res.group('supplier_phones'), res.group('supplier_city')]


class DealLoader(DealLoaderBase):
    supplier_name_in = MapCompose(unicode.strip)
    supplier_address_in = MapCompose(unicode.strip, sanitize_supplier)
    supplier_address_out = Position(3)
    supplier_lat_in = MapCompose(unicode.strip, sanitize_supplier)
    supplier_lat_out = Position(0)
    supplier_lng_in = MapCompose(unicode.strip, sanitize_supplier)
    supplier_lng_out = Position(1)
    supplier_city_in = MapCompose(unicode.strip, sanitize_supplier)
    supplier_city_out = Position(5)
    supplier_phones_in = MapCompose(unicode.strip, sanitize_supplier)
    supplier_phones_out = Position(4)
