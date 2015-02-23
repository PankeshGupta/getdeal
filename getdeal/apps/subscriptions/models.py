# -*- coding: utf-8 -*-
"""
Created on Sep 22, 2013
"""
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db import models


class Subscription(models.Model):
    """
    A feed which a user has subscribed to. Carries all of the cached information
    about the subscription, including unread counts of the three primary scores.
    """
    is_active = models.BooleanField(default=True)
    last_read_date = models.DateTimeField(auto_now=True)
    unread_count_updated = models.DateTimeField(default=now)
    oldest_unread = models.DateTimeField(default=now)
    nbr_rated_deals = models.IntegerField(default=0)
    nbr_positive_deals = models.IntegerField(default=0)
    nbr_negative_deals = models.IntegerField(default=0)
    nbr_shared_deals = models.IntegerField(default=0)
    nbr_viewed_deals = models.IntegerField(default=0)
    nbr_wished_deals = models.IntegerField(default=0)
    nbr_bought_deals = models.IntegerField(default=0)
    nbr_claimed_deals = models.IntegerField(default=0)
    nbr_buried_deals = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def deactivate(self, commit=True):
        self.is_active = False
        if commit:
            self.save()


class CategorySubscription(Subscription):
    user = models.ForeignKey(User, related_name='categories_subscriptions')
    category = models.ForeignKey('categories.Category', related_name='subscribers')

    class Meta:
        verbose_name = _('Category Subscription')
        verbose_name_plural = _('Categories Subscriptions')
        app_label = 'subscriptions'
        unique_together = (('user', 'category'),)

    def __unicode__(self):
        return '%s -> category: %s' % (self.user, self.category)


class SubCategorySubscription(Subscription):
    user = models.ForeignKey(User, related_name='subcategories_subscriptions')
    subcategory = models.ForeignKey('categories.SubCategory', related_name='subscribers')

    class Meta:
        verbose_name = _('SubCategory Subscription')
        verbose_name_plural = _('SubCategories Subscriptions')
        app_label = 'subscriptions'
        unique_together = (('user', 'subcategory'),)

    def __unicode__(self):
        return '%s -> subcategory: %s' % (self.user, self.subcategory)


class CitySubscription(Subscription):
    user = models.ForeignKey(User, related_name='cities_subscriptions')
    city = models.ForeignKey('addresses.City', related_name='subscribers')

    class Meta:
        verbose_name = _('City Subscription')
        verbose_name_plural = _('Cities Subscriptions')
        app_label = 'subscriptions'
        unique_together = (('user', 'city'),)

    def __unicode__(self):
        return '%s -> city: %s' % (self.user, self.city)


class SupplierSubscription(Subscription):
    user = models.ForeignKey(User, related_name='suppliers_subscriptions')
    supplier = models.ForeignKey('suppliers.Supplier', related_name='subscribers')

    class Meta:
        verbose_name = _('Supplier Subscription')
        verbose_name_plural = _('Suppliers Subscriptions')
        app_label = 'subscriptions'
        unique_together = (('user', 'supplier'),)

    def __unicode__(self):
        return '%s -> supplier: %s' % (self.user, self.Supplier)


class DSiteSubscription(Subscription):
    user = models.ForeignKey(User, related_name='dsites_subscriptions')
    dsite = models.ForeignKey('dsites.DSite', related_name='subscribers')

    class Meta:
        verbose_name = _('DSite Subscription')
        verbose_name_plural = _('DSites Subscriptions')
        app_label = 'subscriptions'
        unique_together = (('user', 'dsite'),)

    def __unicode__(self):
        return '%s -> dsite: %s' % (self.user, self.dsite)
