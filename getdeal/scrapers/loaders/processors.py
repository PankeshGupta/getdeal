# -*- coding: utf-8 -*-
"""
Created on Sep 01, 2013
"""
import re

from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import MapCompose, Join, Identity


def encode(value):
    return u"%s".encode('utf-8') % value


def strip_alpha(value):
    return u''.join(re.findall('[\d.?]+', value))


def sanitize_validity(value):
    reg = re.compile(r'(?i).*(du|validit..?:) (?P<validity>.+)', re.UNICODE)
    res = reg.match(value)
    return res.group('validity') if res else None


def sanitize_phones(value):
    reg = re.compile(r'(?P<phones>\d+ \d+ \d+ \d+\s?\d*)', re.UNICODE)
    res = reg.findall(value)
    return [r.strip() for r in res if r.strip()] if res else None


def sanitize_coordinates(value):
    digit_content = u'[\d\.-]+'
    content = u'.+'
    reg = re.compile(r'' + content + '=' + '(?P<lat>' + digit_content + '),' +
                     '(?P<lng>' + digit_content + ')' + content, re.UNICODE)
    res = reg.match(value)
    if res:
        return [res.group('lat'), res.group('lng')]


class Position(object):
    def __init__(self, position=0):
        self.position = position

    def __call__(self, values):
        if values[self.position] is not None and values[self.position] != '':
            return values[self.position]


class DealLoaderBase(XPathItemLoader):
    default_input_processor = MapCompose(unicode.strip)
    default_output_processor = Join()

    title_in = MapCompose(unicode.strip)
    description1_in = MapCompose(unicode.strip)
    description1_out = Join('\n')
    description2_in = MapCompose(unicode.strip)
    description2_out = Join('\n')
    days_in = MapCompose(strip_alpha)
    hours_in = MapCompose(strip_alpha)
    minutes_in = MapCompose(strip_alpha)
    initial_price_in = MapCompose(strip_alpha)
    sell_price_in = MapCompose(strip_alpha)
    discount_in = MapCompose(strip_alpha)
    saving_in = MapCompose(strip_alpha)
    nbr_buyers_in = MapCompose(strip_alpha)
    validity_in = MapCompose(unicode.strip, sanitize_validity)
    cities_in = MapCompose(unicode.strip)
    cities_out = Identity()
    image_urls_out = Identity()
