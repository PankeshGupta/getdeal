# -*- coding: utf-8 -*-
"""
Created on Aug 19, 2013
"""
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.db import models


class Deal(models.Model):
    """
    Deal object
    """
    url = models.URLField(unique=True, max_length=255)
    title = models.CharField(max_length=500)
    description1 = models.TextField(blank=True, null=True)
    description2 = models.TextField(blank=True, null=True)
    sell_price = models.FloatField(default=0.0)
    initial_price = models.FloatField(default=0.0)
    discount = models.FloatField(default=0.0)
    saving = models.FloatField(default=0.0)
    is_valid = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    ends_on = models.DateTimeField(blank=True, null=True)
    validity = models.CharField(max_length=255, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to=settings.IMAGES_STORE+'/full', blank=True, null=True)
    thumbnail = models.ImageField(upload_to=settings.THUMB_STORE, blank=True, null=True, editable=False)
    dsite = models.ForeignKey('dsites.DSite')
    supplier = models.ForeignKey('suppliers.Supplier')
    city = models.ManyToManyField('addresses.City', blank=True, null=True)
    category = models.ForeignKey('categories.Category', blank=True, null=True)
    subcategory = models.ForeignKey('categories.SubCategory', blank=True, null=True)
    current_stats = models.OneToOneField('DealStats', blank=True, null=True, editable=True,
                                         related_name='+')

    class Meta:
        verbose_name = _('Deal')
        verbose_name_plural = _('Deals')
        app_label = 'deals'
        ordering = ['title']

    def __unicode__(self):
        return self.title


class DealStats(models.Model):
    """
    Deal statistics object.
    Every time a deal is scraped, we create a new statistics update about it.
        * The idea is to create a time series.
        * nbr_buyers and nbr_likes : to be scraped from deal site.
        * nbr_views : count the visualisation of the deal.
                    start from previous stats nbr_views (if it exists, keeps increasing).
    """
    deal = models.ForeignKey(Deal, related_name="stats")
    score = models.FloatField(default=0.0)
    nbr_rates = models.IntegerField(default=0)
    nbr_positive_rates = models.IntegerField(default=0)
    nbr_negative_rates = models.IntegerField(default=0)
    nbr_shares = models.IntegerField(default=0)
    nbr_views = models.IntegerField(default=0)
    nbr_wishes = models.IntegerField(default=0)
    nbr_buyers = models.IntegerField(default=0)
    nbr_claims = models.IntegerField(default=0)
    nbr_buries = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    counter = models.IntegerField(default=1, editable=False)
    previous = models.ForeignKey('self', blank=True, null=True, editable=False)

    class Meta:
        verbose_name = _('Deal statistics')
        verbose_name_plural = _('Deals statistics')
        app_label = 'deals'
        ordering = ['deal', '-counter']

    def __unicode__(self):
        return "deal: %s, nbr: %d" % (self.deal.pk, self.counter)

    def save(self, **kwargs):
        current_stats = self.deal.current_stats
        if current_stats is not None and self.id is None:
            self.counter = current_stats.counter + 1
            self.nbr_views = current_stats.nbr_rates
            self.nbr_views = current_stats.nbr_positive_rates
            self.nbr_views = current_stats.nbr_negative_rates
            self.nbr_views = current_stats.nbr_shares
            self.nbr_views = current_stats.nbr_views
            self.nbr_views = current_stats.nbr_wishes
            self.nbr_views = current_stats.nbr_buyers
            self.nbr_views = current_stats.nbr_claims
            self.nbr_views = current_stats.nbr_buries
            self.previous = self.deal.current_stats
        super(DealStats, self).save(**kwargs)


@receiver(post_save, sender=DealStats)
def set_deal_stats(sender, *args, **kwargs):
    """
    Signal handler to ensure that a new stats is always chosen as the current stats - automatically. It simplifies stuff
    greatly. Also stores previous revision for diff-purposes
    """
    instance = kwargs['instance']
    created = kwargs['created']
    if created and instance.deal:
        instance.deal.current_stats = instance
        instance.deal.save()
