# -*- coding: utf-8 -*-
"""
Created on Aug 23, 2013
"""
from model_mommy import mommy

from django.db.utils import IntegrityError
from django.test import TestCase

from apps.dsites.models import DSite
from .models import Address, Country, City, CityMapping, CityStats


class CityTest(TestCase):
    def test_city_creation(self):
        city = mommy.make(City)
        self.assertTrue(isinstance(city, City))
        self.assertEqual(city.__unicode__(), city.name)

    def test_slug_unique(self):
        error_occurred = False
        try:
            mommy.make(City, _quantity=2, name="a", slug="")
        except IntegrityError:
            error_occurred = True
        self.assertTrue(error_occurred)


class MappingTest(TestCase):
    def test_mapping_creation(self):
        mapping = mommy.make(CityMapping)
        self.assertTrue(isinstance(mapping, CityMapping))
        self.assertEqual(mapping.__unicode__(), "Mapping for : %s; %s => %s" %
                                                (mapping.dsite.name,
                                                 mapping.site_city,
                                                 mapping.target_city.name))

    def test_integrity(self):
        dsite = mommy.make(DSite)
        target_city = mommy.make(City)
        site_city = "dummy"
        error_occurred = False
        try:
            mommy.make(CityMapping, _quantity=2, dsite=dsite, site_city=site_city,
                       target_city=target_city)
        except IntegrityError:
            error_occurred = True
        self.assertTrue(error_occurred)

    def test_reverse_mapping(self):
        dsite = mommy.make(DSite)
        cities = mommy.make(City, _quantity=2)
        site_cities = ['dummy1', 'dummy2']
        mommy.make(CityMapping, dsite=dsite, site_city=site_cities[0],
                   target_city=cities[0])
        mommy.make(CityMapping, dsite=dsite, site_city=site_cities[1],
                   target_city=cities[1])
        self.assertEqual(len(dsite.city_mapping.all()), 2)


class CountryTest(TestCase):
    def test_country_creation(self):
        country = mommy.make(Country)
        self.assertTrue(isinstance(country, Country))
        self.assertEqual(country.__unicode__(), country.name)

    def test_slug_unique(self):
        error_occurred = False
        try:
            mommy.make(Country, _quantity=2, name="a", slug="")
        except IntegrityError:
            error_occurred = True
        self.assertTrue(error_occurred)


class AddressTest(TestCase):
    def test_address_creation(self):
        address = mommy.make(Address)
        self.assertTrue(isinstance(address, Address))
        self.assertEqual(address.__unicode__(), address.address)

    def test_empty_address(self):
        address = mommy.make(Address, address='')
        self.assertTrue(isinstance(address, Address))
        self.assertEqual(address.geocode_error, True)

    def test_wrong_address(self):
        address = mommy.make(Address, address='zer jhf @@')
        self.assertTrue(isinstance(address, Address))
        self.assertEqual(address.longitude, None)
        self.assertEqual(address.latitude, None)
        self.assertEqual(address.geocode_error, True)

    def test_correct_address(self):
        museum = 'Natural History Museum, Cromwell Road, London, United Kingdom'
        address = mommy.make(Address, address=museum)
        self.assertTrue(isinstance(address, Address))
        self.assertEqual(address.geocode_error, False)


class CityStatsTest(TestCase):
    def test_city_stats_creation(self):
        city_stats = mommy.make(CityStats)
        self.assertTrue(isinstance(city_stats, CityStats))
        self.assertEqual(city_stats.counter, 1)
        self.assertEqual(city_stats.score, 0.0)
        self.assertEqual(city_stats.previous, None)
        self.assertEqual(city_stats.__unicode__(), "city: %s, counter: %d" %
                                                   (city_stats.city, city_stats.counter))

    def create_two_instance(self):
        city = mommy.make(City)
        city_stats = mommy.make(CityStats, city=city)
        city_stats2 = mommy.make(CityStats, city=city)
        return city, city_stats, city_stats2

    def test_counter_increment(self):
        city, city_stats, city_stats2 = self.create_two_instance()
        self.assertEqual(city_stats.counter, 1)
        self.assertEqual(city_stats2.counter, 2)

    def test_previous(self):
        city, city_stats, city_stats2 = self.create_two_instance()
        self.assertEqual(city_stats.previous, None)
        self.assertEqual(city_stats2.previous, city_stats)
        self.assertEqual(city.current_stats, city_stats2)
