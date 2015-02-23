# -*- coding: utf-8 -*-
"""
Created on Aug 22, 2013
"""
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.statistics.models import StatsBase


class DSite(models.Model):
    """
    Deal site object.
    """
    name = models.CharField(max_length=50, unique=True)
    url = models.URLField(unique=True, max_length=255)
    address1 = models.ForeignKey('addresses.Address', blank=True, null=True, related_name='+')
    address2 = models.ForeignKey('addresses.Address', blank=True, null=True, related_name='+')
    phone1 = models.CharField(max_length=20, blank=True, null=True)
    phone2 = models.CharField(max_length=20, blank=True, null=True)
    phone3 = models.CharField(max_length=20, blank=True, null=True)
    fax = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=150, blank=True, null=True)
    has_validity = models.BooleanField(default=False)
    has_both_mappings = models.BooleanField(default=False)
    has_city_mapping = models.BooleanField(default=False)
    has_category_mapping = models.BooleanField(default=False)
    has_nbr_buyers = models.BooleanField(default=False)
    has_sub_categories = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    current_stats = models.OneToOneField('DSiteStats', blank=True, null=True, editable=True,
                                         related_name='+')

    class Meta:
        verbose_name = _('Deal site')
        verbose_name_plural = _('Deal sites')
        app_label = 'dsites'
        ordering = ['name']

    def __unicode__(self):
        return '%s' % self.name


class DSiteStats(StatsBase):
    """
    Deal site statistics object.
    Get updated periodically to create a time series.
        * nbr_new_deals : nbr newly added deals in this period
        * nbr_active_deals : nbr of active deals in this period
        * nbr_new_suppliers : nbr of newly added suppliers to this deal site (if applicable)
        * suppliers : newly added suppliers to this deal site (if applicable)
        * nbr_likes : nbr of likes from the facebook fan page
        * avg_rating_deals : average rating of active deals in this period
        * avg_quality_suppliers : average rating of suppliers of active deals in this period
        * categories_distribution : this is dictionary; categories + rest.
                                    (those with most deals) form :
                                    "{'top_category_1_id': nbr_deals,
                                     'top_category_2_id': nbr_deals, ...,
                                     'top_category_n_id': nbr_deals, 'rest': nbr_deals}"

        N.B: to know the nbr of suppliers dealing with dsite,
             we sum over all dsitestats.nbr_new_suppliers.
    """
    dsite = models.ForeignKey(DSite, related_name="stats")
    suppliers_distribution = models.ManyToManyField('suppliers.Supplier', blank=True, null=True, related_name='+',
                                                    through='SupplierDistribution')
    cities_distribution = models.ManyToManyField('addresses.City', blank=True, null=True, related_name='+',
                                                 through='CityDistribution')
    categories_distribution = models.ManyToManyField('categories.Category', blank=True, null=True, related_name='+',
                                                     through='CategoryDistribution')
    nbr_likes = models.IntegerField(default=0)
    avg_quality_suppliers = models.FloatField(default=0.0)

    class Meta:
        verbose_name = _('Deal site statistics')
        verbose_name_plural = _('Deal sites statistics')
        app_label = 'dsites'
        ordering = ['dsite', '-counter']

    def __unicode__(self):
        return 'dsite: %s, counter: %d' % (self.dsite, self.counter)

    def save(self, **kwargs):
        current_stats = self.dsite.current_stats
        if current_stats is not None and self.id is None:
            self.counter = current_stats.counter + 1
            self.previous = self.dsite.current_stats
        super(DSiteStats, self).save(**kwargs)

    def increment_new_by(self, nbr_deals):
        self.nbr_new_deals += int(nbr_deals)

    def increment_active_by(self, nbr_deals):
        self.nbr_active_deals += int(nbr_deals)
        

class Distribution(models.Model):
    """
    abstract class to track nbr nex deals for stats period
    """
    stats = models.ForeignKey('DSiteStats', related_name='+')
    nbr_deals = models.IntegerField(default=0)

    class Meta:
        abstract = True
        ordering = ['stats']

    def increment_by(self, nbr_deals):
        self.nbr_deals += int(nbr_deals)


class SupplierDistribution(Distribution):
    """
    Supplier distribution: tracks deals' suppliers for this stats period
    """
    supplier = models.ForeignKey('suppliers.Supplier', related_name='+')
    is_new = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Suppliers Distribution')
        verbose_name_plural = _('Suppliers Distribution')
        app_label = 'dsites'

    def __unicode__(self):
        return '%s -> supplier: %s' % (self.stats, self.supplier)


class CityDistribution(Distribution):
    """
    City distribution: tracks deals' cities for this stats period
    """
    city = models.ForeignKey('addresses.City', related_name='+')

    class Meta:
        verbose_name = _('Cities Distribution')
        verbose_name_plural = _('Cities Distribution')
        app_label = 'dsites'

    def __unicode__(self):
        return '%s -> city: %s' % (self.stats, self.city)


class CategoryDistribution(Distribution):
    """
    Categories distribution: tracks deals' categories for this stats period
    """
    category = models.ForeignKey('categories.Category', related_name='+')

    class Meta:
        verbose_name = _('Categories Distribution')
        verbose_name_plural = _('Categories Distribution')
        app_label = 'dsites'

    def __unicode__(self):
        return u'%s -> category: %s' % (self.stats, self.category)


@receiver(post_save, sender=DSiteStats)
def set_dsite_stats(sender, *args, **kwargs):
    """Signal handler to ensure that a new stats is always chosen as the
    current stats - automatically. It simplifies stuff greatly. Also
    stores previous revision for diff-purposes"""
    instance = kwargs['instance']
    created = kwargs['created']
    if created and instance.dsite:
        instance.dsite.current_stats = instance
        instance.dsite.save()
