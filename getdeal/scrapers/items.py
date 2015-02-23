# -*- coding: utf-8 -*-
"""
Created on Aug 25, 2013
"""
from scrapy.contrib.djangoitem import DjangoItem
from scrapy.item import Field

from apps.deals.models import Deal, DealStats
from apps.addresses.models import Address, City
from apps.suppliers.models import Supplier
from apps.categories.models import CategoryMapping


class DealItem(DjangoItem):
    django_model = Deal
    is_new = Field()
    days = Field()
    hours = Field()
    minutes = Field()
    nbr_buyers = Field()
    supplier_new = Field()
    supplier_name = Field()
    supplier_address = Field()
    supplier_lat = Field()
    supplier_lng = Field()
    supplier_city = Field()
    supplier_phones = Field()
    cities = Field()
    image_urls = Field()
    images = Field()

    def save(self, spider, commit=True):
        if self.get('supplier_name', None) is not None:
            #only add supplier if it exists
            self.add_supplier()
        self.add_category(spider)
        self.add_image()
        instance = super(DealItem, self).save(commit=commit)
        self.add_cities(spider)
        self.add_stats()
        return instance

    def set_instance(self, instance):
        self._instance = instance

    def add_image(self):
        #self.instance.image = File(open(settings.IMAGES_STORE + self['images'][0]['path'], 'r'))
        self.instance.image = self['images'][0]['path']

    def add_supplier(self):
        address = None
        if self.get('supplier_address', None) is not None:
            try:
                address = Address.objects.get(address=self['supplier_address'])
                if address.geocode_error:
                    try:
                        longitude = self['supplier_lng']
                        latitude = self['supplier_lat']
                        address.longitude = longitude
                        address.latitude = latitude
                        address.geocode_error = False
                        address.save()
                    except:
                        pass
            except:
                address, _ = Address.objects.get_or_create(address=self['supplier_address'],
                                                           longitude=self.get('supplier_lng', None),
                                                           latitude=self.get('supplier_lat', None))
        if Supplier.objects.filter(name=self['supplier_name']).exists():
            supplier = Supplier.objects.get(name=self['supplier_name'])
            self['supplier_new'] = False
        else:
            phones = [''] * 3
            try:
                for ind, val in enumerate(self['supplier_phones'].split('-')):
                    phones[ind] = val
            except:
                pass
            supplier, _ = Supplier.objects.get_or_create(name=self['supplier_name'],
                                                         address1=address, phone1=phones[0],
                                                         phone2=phones[1], phone3=phones[2])
            self['supplier_new'] = True
        self['supplier'] = supplier

    def add_category(self, spider):
        if spider.category_mapping is not None:
            self['category'] = spider.category_mapping.target_category
        else:
            #we check if we updated this field through the page scraping
            try:
                self['category'] = CategoryMapping.objects.get(dsite=spider.dsite,
                                                               site_category=self['category']).target_category
            except:
                self['category'] = None

    def add_cities(self, spider):
        if spider.city_mapping:
            self.instance.city.add(spider.city_mapping.target_city)
        else:
            #we check if we updated this field through the page scraping
            try:
                for city in [City.objects.get(slug=city) for city in self['cities'] if
                             City.objects.filter(slug=city).exists()]:
                    self.instance.city.add(city)
            except:
                pass

    def add_stats(self):
        DealStats.objects.create(deal=self.instance, nbr_buyers=self.get('nbr_buyers', 0))
