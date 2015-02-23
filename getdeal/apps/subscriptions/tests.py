# -*- coding: utf-8 -*-
"""
Created on Sep 25, 2013
"""
from model_mommy import mommy

from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.test import TestCase


from apps.addresses.models import City
from apps.categories.models import Category, SubCategory, CategoryStats
from apps.dsites.models import DSite
from apps.profiles.models import Profile, ProfileStats
from apps.suppliers.models import Supplier
from .models import CategorySubscription, SubCategorySubscription, CitySubscription, SupplierSubscription, DSiteSubscription


class SubscriptionTest(TestCase):
    def test_list_creation(self):
        subscription = mommy.prepare(CategorySubscription)
        self.assertTrue(isinstance(subscription, CategorySubscription))
        subscription = mommy.prepare(SubCategorySubscription)
        self.assertTrue(isinstance(subscription, SubCategorySubscription))
        subscription = mommy.prepare(CitySubscription)
        self.assertTrue(isinstance(subscription, CitySubscription))
        subscription = mommy.prepare(SupplierSubscription)
        self.assertTrue(isinstance(subscription, SupplierSubscription))
        subscription = mommy.prepare(DSiteSubscription)
        self.assertTrue(isinstance(subscription, DSiteSubscription))

    def create_user(self):
        profile = Profile.objects.get(user=mommy.make(User))
        mommy.make(ProfileStats, profile=profile)
        return profile

    def test_integrity_category(self):
        profile = self.create_user()
        category = mommy.make(Category)
        mommy.make(CategoryStats, category=category)
        integrity_error = False
        try:
            mommy.make(CategorySubscription, _quantity=3, user=profile.user, category=category)
        except IntegrityError:
            integrity_error = True
        self.assertTrue(integrity_error)

    def test_integrity_subcategory(self):
        profile = self.create_user()
        subcategory = mommy.make(SubCategory)
        integrity_error = False
        try:
            mommy.make(SubCategorySubscription, _quantity=3, user=profile.user, subcategory=subcategory)
        except IntegrityError:
            integrity_error = True
        self.assertTrue(integrity_error)

    def test_integrity_city(self):
        profile = self.create_user()
        city = mommy.make(City)
        integrity_error = False
        try:
            mommy.make(CitySubscription, _quantity=3, user=profile.user, city=city)
        except IntegrityError:
            integrity_error = True
        self.assertTrue(integrity_error)

    def test_integrity_supplier(self):
        profile = self.create_user()
        supplier = mommy.make(Supplier)
        integrity_error = False
        try:
            mommy.make(SupplierSubscription, _quantity=3, user=profile.user, supplier=supplier)
        except IntegrityError:
            integrity_error = True
        self.assertTrue(integrity_error)

    def test_integrity_dsite(self):
        profile = self.create_user()
        dsite = mommy.make(DSite)
        integrity_error = False
        try:
            mommy.make(DSiteSubscription, _quantity=3, user=profile.user, dsite=dsite)
        except IntegrityError:
            integrity_error = True
        self.assertTrue(integrity_error)

    def test_deactivate(self):
        category_subscription = mommy.prepare(CategorySubscription)
        subcategory_subscription = mommy.prepare(SubCategorySubscription)
        city_subscription = mommy.prepare(CitySubscription)
        supplier_subscription = mommy.prepare(SupplierSubscription)
        dsite_subscription = mommy.prepare(DSiteSubscription)
        self.assertTrue(category_subscription.is_active)
        self.assertTrue(subcategory_subscription.is_active)
        self.assertTrue(city_subscription.is_active)
        self.assertTrue(supplier_subscription.is_active)
        self.assertTrue(dsite_subscription.is_active)
        category_subscription.deactivate(commit=False)
        subcategory_subscription.deactivate(commit=False)
        city_subscription.deactivate(commit=False)
        supplier_subscription.deactivate(commit=False)
        dsite_subscription.deactivate(commit=False)
        self.assertFalse(category_subscription.is_active)
        self.assertFalse(subcategory_subscription.is_active)
        self.assertFalse(city_subscription.is_active)
        self.assertFalse(supplier_subscription.is_active)
        self.assertFalse(dsite_subscription.is_active)
