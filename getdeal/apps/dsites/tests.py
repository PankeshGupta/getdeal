# -*- coding: utf-8 -*-
"""
Created on Aug 22, 2013
"""
from model_mommy import mommy

from django.test import TestCase

from .models import DSite, DSiteStats, SupplierDistribution, CategoryDistribution, CityDistribution


class DSiteTest(TestCase):

    def test_dsite_creation(self):
        dsite = mommy.make(DSite)
        self.assertTrue(isinstance(dsite, DSite))
        self.assertEqual(dsite.__unicode__(), dsite.name)
        self.assertEqual(dsite.current_stats, None)


class DSiteStatsTest(TestCase):

    def test_dsite_stats_creation(self):
        dsite_stats = mommy.make(DSiteStats)
        self.assertTrue(isinstance(dsite_stats, DSiteStats))
        self.assertEqual(dsite_stats.counter, 1)
        self.assertEqual(dsite_stats.score, 0.0)
        self.assertEqual(dsite_stats.previous, None)
        self.assertEqual(dsite_stats.__unicode__(), "dsite: %s, counter: %d" %
                                                    (dsite_stats.dsite, dsite_stats.counter))

    def create_two_instance(self):
        dsite = mommy.make(DSite)
        dsite_stats = mommy.make(DSiteStats, dsite=dsite)
        deal_stats2 = mommy.make(DSiteStats, dsite=dsite)
        return dsite, dsite_stats, deal_stats2

    def test_counter_increment(self):
        dsite, dsite_stats, dsite_stats2 = self.create_two_instance()
        self.assertEqual(dsite_stats.counter, 1)
        self.assertEqual(dsite_stats2.counter, 2)

    def test_previous(self):
        dsite, dsite_stats, dsite_stats2 = self.create_two_instance()
        self.assertEqual(dsite_stats.previous, None)
        self.assertEqual(dsite_stats2.previous, dsite_stats)
        self.assertEqual(dsite.current_stats, dsite_stats2)

    def test_distribution(self):
        stats = mommy.make(DSiteStats)
        category_distibution = mommy.make(CategoryDistribution, stats=stats)
        supplier_distribution = mommy.make(SupplierDistribution, stats=stats)
        city_distribution = mommy.make(CityDistribution, stats=stats)
        self.assertEqual(category_distibution.stats, stats)
        self.assertEqual(supplier_distribution.stats, stats)
        self.assertEqual(city_distribution.stats, stats)
        self.assertEqual(category_distibution.nbr_deals, 0)
        self.assertEqual(supplier_distribution.nbr_deals, 0)
        self.assertEqual(city_distribution.nbr_deals, 0)
        category_distibution.increment_by(3)
        supplier_distribution.increment_by(1)
        city_distribution.increment_by(10)
        self.assertEqual(category_distibution.nbr_deals, 3)
        self.assertEqual(supplier_distribution.nbr_deals, 1)
        self.assertEqual(city_distribution.nbr_deals, 10)
        category_distibution.increment_by(3)
        supplier_distribution.increment_by(1)
        city_distribution.increment_by(10)
        self.assertEqual(category_distibution.nbr_deals, 6)
        self.assertEqual(supplier_distribution.nbr_deals, 2)
        self.assertEqual(city_distribution.nbr_deals, 20)
