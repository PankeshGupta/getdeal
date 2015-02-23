# -*- coding: utf-8 -*-
"""
Created on Aug 23, 2013
"""
from model_mommy import mommy

from django.db.utils import IntegrityError
from django.test import TestCase


from apps.dsites.models import DSite
from .models import (Category, CategoryMapping, SubCategory, SubCategoryMapping,
                     CategoryStats, SubCategoryStats)


class CategoryTest(TestCase):
    def test_category_creation(self):
        category = mommy.make(Category)
        self.assertTrue(isinstance(category, Category))
        self.assertEqual(category.__unicode__(), category.name)

    def test_slug_unique(self):
        error_occurred = False
        try:
            mommy.make(Category, _quantity=2, name="a", slug="")
        except IntegrityError:
            error_occurred = True
        self.assertTrue(error_occurred)


class CategoryMappingTest(TestCase):
    def test_mapping_creation(self):
        mapping = mommy.make(CategoryMapping)
        self.assertTrue(isinstance(mapping, CategoryMapping))
        self.assertEqual(mapping.__unicode__(), "Mapping for : %s; %s => %s" %
                                                (mapping.dsite.name,
                                                 mapping.site_category,
                                                 mapping.target_category.name))

    def test_integrity(self):
        dsite = mommy.make(DSite)
        target_category = mommy.make(Category)
        site_category = "dummy"
        error_occurred = False
        try:
            mommy.make(CategoryMapping, _quantity=2, dsite=dsite, site_category=site_category,
                       target_category=target_category)
        except IntegrityError:
            error_occurred = True
        self.assertTrue(error_occurred)

    def test_reverse_mapping(self):
        dsite = mommy.make(DSite)
        categories = mommy.make(Category, _quantity=2)
        site_categories = ['dummy1', 'dummy2']
        mommy.make(CategoryMapping, dsite=dsite, site_category=site_categories[0],
                   target_category=categories[0])
        mommy.make(CategoryMapping, dsite=dsite, site_category=site_categories[1],
                   target_category=categories[1])
        self.assertEqual(len(dsite.category_mapping.all()), 2)


class SubCategoryTest(TestCase):
    def test_subcategory_creation(self):
        subcategory = mommy.make(SubCategory)
        self.assertTrue(isinstance(subcategory, SubCategory))
        self.assertEqual(subcategory.__unicode__(), subcategory.name)

    def test_slug_unique(self):
        error_occurred = False
        try:
            mommy.make(SubCategory, _quantity=2, name="a", slug="")
        except IntegrityError:
            error_occurred = True
        self.assertTrue(error_occurred)


class SubCategoryMappingTest(TestCase):
    def test_submapping_creation(self):
        submapping = mommy.make(SubCategoryMapping)
        self.assertTrue(isinstance(submapping, SubCategoryMapping))
        self.assertEqual(submapping.__unicode__(), "SubMapping for : %s; %s => %s" %
                                                   (submapping.dsite.name,
                                                    submapping.site_subcategory,
                                                    submapping.target_subcategory.name))

    def test_slug_unique(self):
        dsite = mommy.make(DSite)
        target_subcategory = mommy.make(SubCategory)
        site_subcategory = 'dummy'
        error_occurred = False
        try:
            mommy.make(SubCategoryMapping, _quantity=2, dsite=dsite, site_subcategory=site_subcategory,
                       target_subcategory=target_subcategory)
        except IntegrityError:
            error_occurred = True
        self.assertTrue(error_occurred)

    def test_reverse_submapping(self):
        dsite = mommy.make(DSite)
        subcategories = mommy.make(SubCategory, _quantity=2)
        site_subcategories = ['dummy1', 'dummy2']
        mommy.make(SubCategoryMapping, dsite=dsite, site_subcategory=site_subcategories[0],
                   target_subcategory=subcategories[0])
        mommy.make(SubCategoryMapping, dsite=dsite, site_subcategory=site_subcategories[1],
                   target_subcategory=subcategories[1])
        self.assertEqual(len(dsite.subcategory_mapping.all()), 2)


class CategoryStatsTest(TestCase):

    def test_city_stats_creation(self):
        category_stats = mommy.make(CategoryStats)
        self.assertTrue(isinstance(category_stats, CategoryStats))
        self.assertEqual(category_stats.counter, 1)
        self.assertEqual(category_stats.score, 0.0)
        self.assertEqual(category_stats.previous, None)
        self.assertEqual(category_stats.__unicode__(),
                         "category: %s, counter: %d" % (category_stats.category, category_stats.counter))

    def create_two_instance(self):
        category = mommy.make(Category)
        category_stats = mommy.make(CategoryStats, category=category)
        category_stats2 = mommy.make(CategoryStats, category=category)
        return category, category_stats, category_stats2

    def test_counter_increment(self):
        category, category_stats, category_stats2 = self.create_two_instance()
        self.assertEqual(category_stats.counter, 1)
        self.assertEqual(category_stats2.counter, 2)

    def test_previous(self):
        category, category_stats, category_stats2 = self.create_two_instance()
        self.assertEqual(category_stats.previous, None)
        self.assertEqual(category_stats2.previous, category_stats)
        self.assertEqual(category.current_stats, category_stats2)


class SubCategoryStatsTest(TestCase):

    def test_city_stats_creation(self):
        subcategory_stats = mommy.make(SubCategoryStats)
        self.assertTrue(isinstance(subcategory_stats, SubCategoryStats))
        self.assertEqual(subcategory_stats.counter, 1)
        self.assertEqual(subcategory_stats.score, 0.0)
        self.assertEqual(subcategory_stats.previous, None)
        self.assertEqual(subcategory_stats.__unicode__(),
                         "subcategory: %s, counter: %d" % (subcategory_stats.subcategory, subcategory_stats.counter))

    def create_two_instance(self):
        subcategory = mommy.make(SubCategory)
        subcategory_stats = mommy.make(SubCategoryStats, subcategory=subcategory)
        subcategory_stats2 = mommy.make(SubCategoryStats, subcategory=subcategory)
        return subcategory, subcategory_stats, subcategory_stats2

    def test_counter_increment(self):
        subcategory, subcategory_stats, subcategory_stats2 = self.create_two_instance()
        self.assertEqual(subcategory_stats.counter, 1)
        self.assertEqual(subcategory_stats2.counter, 2)

    def test_previous(self):
        subcategory, subcategory_stats, subcategory_stats2 = self.create_two_instance()
        self.assertEqual(subcategory_stats.previous, None)
        self.assertEqual(subcategory_stats2.previous, subcategory_stats)
        self.assertEqual(subcategory.current_stats, subcategory_stats2)
