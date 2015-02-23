# -*- coding: utf-8 -*-
"""
Created on Aug 23, 2013
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.template.defaultfilters import slugify

from apps.statistics.models import StatsBase


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, verbose_name=_('slug'), unique=True)
    current_stats = models.OneToOneField('CategoryStats', blank=True, null=True, editable=True,
                                         related_name='+')

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        app_label = 'categories'
        ordering = ['name']

    def __unicode__(self):
        return "%s" % self.name

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class CategoryMapping(models.Model):
    """
    Mapping between deal site categories and internal categories
    """
    dsite = models.ForeignKey('dsites.DSite', related_name='category_mapping')
    target_category = models.ForeignKey('Category', related_name='mapping')
    site_category = models.CharField(max_length=100)
    all_cities = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Category mapping')
        verbose_name_plural = _('Category mappings')
        app_label = 'categories'
        unique_together = (('dsite', 'site_category', 'target_category'),)
        ordering = ['dsite']

    def __unicode__(self):
        return "Mapping for : %s; %s => %s" % (self.dsite.name,
                                               self.site_category,
                                               self.target_category.name)


class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, verbose_name=_('slug'), unique=True)
    parent = models.ForeignKey('Category')
    current_stats = models.OneToOneField('SubCategoryStats', blank=True, null=True, editable=True,
                                         related_name='+')

    class Meta:
        verbose_name = _('Subcategory')
        verbose_name_plural = _('Subcategories')
        app_label = 'categories'
        ordering = ['name']

    def __unicode__(self):
        return "%s" % self.name

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            self.slug = slugify(self.name)
        super(SubCategory, self).save(*args, **kwargs)


class SubCategoryMapping(models.Model):
    """
    Mapping between deal site subcategories and internal subcategories
    """
    dsite = models.ForeignKey('dsites.DSite', related_name='subcategory_mapping')
    target_subcategory = models.ForeignKey('SubCategory', related_name='site_submapping')
    site_subcategory = models.CharField(max_length=100)
    all_cities = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Subcategory mapping')
        verbose_name_plural = _('Subcategory mappings')
        app_label = 'categories'
        unique_together = (('dsite', 'site_subcategory', 'target_subcategory'),)
        ordering = ['dsite']

    def __unicode__(self):
        return "SubMapping for : %s; %s => %s" % (self.dsite.name,
                                                  self.site_subcategory,
                                                  self.target_subcategory.name)


class CategoryStats(StatsBase):
    """
    Category statistics object.
    Get updated periodically to create a time series.
    """
    category = models.ForeignKey(Category, related_name="stats")

    class Meta:
        verbose_name = _('Category statistics')
        verbose_name_plural = _('Categories statistics')
        app_label = 'categories'
        ordering = ['category', '-counter']

    def __unicode__(self):
        return "category: %s, counter: %d" % (self.category, self.counter)

    def save(self, **kwargs):
        current_stats = self.category.current_stats
        if current_stats is not None and self.id is None:
            self.counter = current_stats.counter + 1
            self.previous = self.category.current_stats
        super(CategoryStats, self).save(**kwargs)


@receiver(post_save, sender=CategoryStats)
def set_category_stats(sender, *args, **kwargs):
    """Signal handler to ensure that a new stats is always chosen as the
    current stats - automatically. It simplifies stuff greatly. Also
    stores previous revision for diff-purposes"""
    instance = kwargs['instance']
    created = kwargs['created']
    if created and instance.category:
        instance.category.current_stats = instance
        instance.category.save()


class SubCategoryStats(StatsBase):
    """
    SubCategory statistics object.
    Get updated periodically to create a time series.
    """
    subcategory = models.ForeignKey(SubCategory, related_name="stats")

    class Meta:
        verbose_name = _('Subcategory statistics')
        verbose_name_plural = _('Subcategories statistics')
        app_label = 'categories'
        ordering = ['subcategory', '-counter']

    def __unicode__(self):
        return "subcategory: %s, counter: %d" % (self.subcategory, self.counter)

    def save(self, **kwargs):
        current_stats = self.subcategory.current_stats
        if current_stats is not None and self.id is None:
            self.counter = current_stats.counter + 1
            self.previous = self.subcategory.current_stats
        super(SubCategoryStats, self).save(**kwargs)


@receiver(post_save, sender=SubCategoryStats)
def set_subcategory_stats(sender, *args, **kwargs):
    """Signal handler to ensure that a new stats is always chosen as the
    current stats - automatically. It simplifies stuff greatly. Also
    stores previous revision for diff-purposes"""
    instance = kwargs['instance']
    created = kwargs['created']
    if created and instance.subcategory:
        instance.subcategory.current_stats = instance
        instance.subcategory.save()
