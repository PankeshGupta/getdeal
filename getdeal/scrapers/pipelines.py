# -*- coding: utf-8 -*-
"""
Created on Aug 25, 2013
"""
import datetime
from urlparse import urljoin

from django.utils.timezone import now

from scrapy import signals
from scrapy.exceptions import DropItem

from apps.deals.models import Deal
from apps.dsites.models import CityDistribution, CategoryDistribution, SupplierDistribution


class CheckPipeline(object):
    """
    Check if the current item exist in database
    """

    def process_item(self, item, spider):
        item['is_new'] = True
        try:
            #See if the deal already exists, If so then try to update cities
            #N.B : One deal can exists in multiple cities
            deal = Deal.objects.get(url=item['url'])
            item['is_new'] = False
            item.set_instance(deal)
            item.add_cities(spider)
            if not spider.updating:
                raise DropItem("Not updating")
            return item
        except DropItem:
            raise DropItem("Not updating")
        except:
            return item


class CleanPipeline(object):
    """
    Ensure that the item fields are cleaned, and the item is valid
    """

    def process_item(self, item, spider):
        if item['is_new']:
            item['dsite'] = spider.dsite
            try:
                days = item.get('days', 0)
                time_delta = datetime.timedelta(days=int(days), hours=int(item['hours']), minutes=int(item['minutes']))
                item['ends_on'] = now() + time_delta
            except:
                item['is_valid'] = False
            self.convert_float(item, 'discount')
            self.convert_float(item, 'initial_price')
            self.convert_float(item, 'sell_price')
            self.convert_float(item, 'saving')
            if item['saving'] == 0.0:
                item['saving'] = item['initial_price'] - item['sell_price']
        self.convert_int(item, 'nbr_buyers')
        self.clean_url(item, spider, 'image_urls')
        return item

    def convert_int(self, item, value):
        try:
            item[value] = int(item[value])
        except:
            item[value] = 0

    def convert_float(self, item, value):
        try:
            item[value] = float(item[value])
        except:
            item[value] = 0.0

    def clean_url(self, item, spider, value):
        try:
            item[value] = [urljoin(spider.dsite.url, url) for url in item[value]]
        except:
            pass


class SerializePipeline(object):
    """
    Serialize this item and update the number of saved items for this spider
    """

    def __init__(self, stats):
        self.stats = stats
        self.suppliers = []
        self.categories = []
        self.cities = []

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.stats)
        crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)
        return o

    def spider_closed(self, spider):
        self.stats.set_value('suppliers', set(self.suppliers), spider=spider)
        self.stats.set_value('categories', set(self.categories), spider=spider)
        self.stats.set_value('cities', set(self.cities), spider=spider)

    def process_item(self, item, spider):
        if item['is_new']:
            item.save(spider)
            self.suppliers.append((item.instance.supplier, item['supplier_new']))
            self.stats.inc_value(item.instance.supplier, spider=spider)
            self.categories.append(item.instance.category)
            self.stats.inc_value(item.instance.category, spider=spider)
            for city in item.instance.city.all():
                self.cities.append(city)
                self.stats.inc_value(city, spider=spider)
            self.stats.inc_value('nbr_new_deals', spider=spider)
        else:
            item.add_stats()
            self.stats.inc_value('items_update_count', spider=spider)
        return item


class StatsCollectionPipeline(object):
    """
    Collect stats, connects to the spider_closed signal, also does some cleaning of keys.
    Quite the spider driver before finishing
    """

    def __init__(self, stats):
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.stats)
        crawler.signals.connect(o.collect_stats, signal=signals.spider_closed)
        return o

    def collect_stats(self, spider):
        spider.dsite.current_stats.increment_new_by(self.stats.get_value('nbr_new_deals', 0))
        spider.dsite.current_stats.save()
        for category in self.stats.get_value('categories'):
            if category is not None:
                current_categories_distribution, _ = CategoryDistribution.objects.get_or_create(
                    stats=spider.dsite.current_stats,
                    category=category)
                current_categories_distribution.increment_by(self.stats.get_value(category))
                current_categories_distribution.save()
        for city in self.stats.get_value('cities'):
            if city is not None:
                current_cities_distribution, _ = CityDistribution.objects.get_or_create(
                    stats=spider.dsite.current_stats,
                    city=city)
                current_cities_distribution.increment_by(self.stats.get_value(city))
                current_cities_distribution.save()
        for (supplier, is_new) in self.stats.get_value('suppliers'):
            if supplier is not None:
                current_suppliers_distribution, created = SupplierDistribution.objects.get_or_create(
                    stats=spider.dsite.current_stats,
                    supplier=supplier)
                current_suppliers_distribution.increment_by(self.stats.get_value(supplier))
                if created:
                    current_suppliers_distribution.is_new = True if is_new else False
                current_suppliers_distribution.save()
        spider.quit_driver()

    def process_item(self, item, spider):
        item['supplier'] = item['supplier'].id if item.get('supplier', '') else ''
        item['category'] = item['category'].id if item.get('category') else ''
        item['dsite'] = item['dsite'].id if item.get('dsite') else ''
        return item
