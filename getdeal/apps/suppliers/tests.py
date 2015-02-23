# -*- coding: utf-8 -*-
"""
Created on Aug 22, 2013
"""

from django.test import TestCase
from django.core.urlresolvers import reverse
from model_mommy import mommy
from suppliers.models import Supplier, SupplierStats


class SupplierTest(TestCase):
    def test_supplier_creation(self):
        supplier = mommy.make(Supplier)
        self.assertTrue(isinstance(supplier, Supplier))
        self.assertEqual(supplier.__unicode__(), supplier.name)
        self.assertEqual(supplier.current_stats, None)

    def test_deal_slug(self):
        supplier = mommy.make(Supplier, name="a", slug="")
        supplier2 = mommy.make(Supplier, name="a", slug="")
        self.assertEqual(supplier.slug, "a")
        self.assertEqual(supplier2.slug, "a1")


class SupplierStatsTest(TestCase):
    def test_supplier_stats_creation(self):
        supplier_stats = mommy.make(SupplierStats)
        self.assertTrue(isinstance(supplier_stats, SupplierStats))
        self.assertEqual(supplier_stats.counter, 1)
        self.assertEqual(supplier_stats.score, 0.0)
        self.assertEqual(supplier_stats.previous, None)
        self.assertEqual(supplier_stats.__unicode__(), "supplier: %s, counter: %d" %
                                                       (supplier_stats.supplier, supplier_stats.counter))

    def create_two_instance(self):
        supplier = mommy.make(Supplier)
        supplier_stats = mommy.make(SupplierStats, supplier=supplier)
        supplier_stats2 = mommy.make(SupplierStats, supplier=supplier)
        return supplier, supplier_stats, supplier_stats2

    def test_counter_increment(self):
        supplier, supplier_stats, supplier_stats2 = self.create_two_instance()
        self.assertEqual(supplier_stats.counter, 1)
        self.assertEqual(supplier_stats2.counter, 2)

    def test_previous(self):
        supplier, supplier_stats, supplier_stats2 = self.create_two_instance()
        self.assertEqual(supplier_stats.previous, None)
        self.assertEqual(supplier_stats2.previous, supplier_stats)
        self.assertEqual(supplier.current_stats, supplier_stats2)
