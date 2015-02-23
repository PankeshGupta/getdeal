# -*- coding: utf-8 -*-
"""
Created on Aug 23, 2013
"""
import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.template.defaultfilters import slugify

from apps.statistics.models import StatsBase
from .utils import google_v3, GeoError

logger = logging.getLogger(__name__)


class Address(models.Model):
    """
    Address object
    """
    address = models.CharField(_('Address'), max_length=255, unique=True)
    computed_address = models.CharField(_('Computed address'), max_length=255, null=True, blank=True)
    latitude = models.FloatField(_('Latitude'), null=True, blank=True)
    longitude = models.FloatField(_('Longitude'), null=True, blank=True)
    geocode_error = models.BooleanField(_('Geocode error'), default=False)

    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')
        app_label = 'addresses'

    def __unicode__(self):
        return self.address

    def fill_geocode_data(self):
        if not self.address:
            self.geocode_error = True
            return
        try:
            self.computed_address, (self.latitude, self.longitude,) = google_v3(self.address)
            self.geocode_error = False
        except GeoError as e:
            try:
                logger.error(e)
            except Exception:
                logger.error("Geocoding error for address %s", self.address)
            self.geocode_error = True

    def save(self, *args, **kwargs):
        # fill geocode data if it is unknown
        if (self.longitude is None) or (self.latitude is None):
            self.fill_geocode_data()
        super(Address, self).save(*args, **kwargs)


class Country(models.Model):
    """
    Country object
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, verbose_name=_('slug'), unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')
        app_label = 'addresses'

    def __unicode__(self):
        return "%s" % self.name

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            self.slug = slugify(self.name)
        super(Country, self).save(*args, **kwargs)


class City(models.Model):
    """
    this class descibes mediacal Cities
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, verbose_name=_('slug'), unique=True)
    abbreviation = models.CharField(max_length=80, null=True, blank=True)
    country = models.ForeignKey(Country)
    is_active = models.BooleanField(default=True)
    current_stats = models.OneToOneField('CityStats', blank=True, null=True, editable=True,
                                         related_name='+')

    class Meta:
        verbose_name = _('City')
        verbose_name_plural = _('Cities')
        app_label = 'addresses'

    def __unicode__(self):
        return "%s" % self.name

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            self.slug = slugify(self.name)
        super(City, self).save(*args, **kwargs)


class CityMapping(models.Model):
    """
    Mapping between deal site cities and internal cities
    """
    dsite = models.ForeignKey('dsites.DSite', related_name='city_mapping')
    target_city = models.ForeignKey('City', related_name='mapping')
    site_city = models.CharField(max_length=100)

    class Meta:
        verbose_name = _('City mapping')
        verbose_name_plural = _('City mappings')
        app_label = 'addresses'
        unique_together = (('dsite', 'site_city', 'target_city'),)
        ordering = ['dsite']

    def __unicode__(self):
        return "Mapping for : %s; %s => %s" % (self.dsite.name,
                                               self.site_city,
                                               self.target_city.name)


class CityStats(StatsBase):
    """
    City statistics object.
    Get updated periodically to create a time series.
    """
    city = models.ForeignKey(City, related_name="stats")

    class Meta:
        verbose_name = _('City statistics')
        verbose_name_plural = _('Cities statistics')
        app_label = 'addresses'
        ordering = ['city', '-counter']

    def __unicode__(self):
        return "city: %s, counter: %d" % (self.city, self.counter)

    def save(self, **kwargs):
        current_stats = self.city.current_stats
        if current_stats is not None and self.id is None:
            self.counter = current_stats.counter + 1
            self.previous = self.city.current_stats
        super(CityStats, self).save(**kwargs)


@receiver(post_save, sender=CityStats)
def set_city_stats(sender, *args, **kwargs):
    """Signal handler to ensure that a new stats is always chosen as the
    current stats - automatically. It simplifies stuff greatly. Also
    stores previous revision for diff-purposes"""
    instance = kwargs['instance']
    created = kwargs['created']
    if created and instance.city:
        instance.city.current_stats = instance
        instance.city.save()
