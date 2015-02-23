# -*- coding: utf-8 -*-
"""
Created on Aug 22, 2013
"""
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify

from apps.statistics.models import StatsBase


class Supplier(models.Model):
    """
    Supplier object
    """
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True)
    address1 = models.ForeignKey('addresses.Address', blank=True, null=True, related_name='+')
    address2 = models.ForeignKey('addresses.Address', blank=True, null=True, related_name='+')
    phone1 = models.CharField(max_length=20)
    phone2 = models.CharField(max_length=20)
    phone3 = models.CharField(max_length=20)
    fax = models.CharField(max_length=20)
    email = models.EmailField(max_length=150)
    info = models.TextField()
    current_stats = models.OneToOneField('SupplierStats', blank=True, null=True, editable=True,
                                         related_name='+')

    class Meta:
        verbose_name = _('Deal supplier')
        verbose_name_plural = _('Deal suppliers')
        app_label = 'suppliers'
        ordering = ['name']

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            slug = slugify(self.name)
            supplier_cnt = Supplier.objects.filter(slug__startswith=slug).count()
            if supplier_cnt > 0:
                slug += str(supplier_cnt)
            self.slug = slug
        super(Supplier, self).save(*args, **kwargs)


class SupplierStats(StatsBase):
    """
    Supplier statistics object.
    Get updated periodically to create a time series.
        * rating_yelp : rating of the supplier on yelp (if applicable)
        * rating_tripadvisor : rating of the supplier on tripadvisor (if applicable)
        * nbr_new_dsites : nbr of new sites showing deals of this supplier (if applicable)
        * dsites : new sites showing deals of this supplier (if applicable)

        N.B: to know the nbr of deal sites showing deals for this supplier,
             we sum over all supplierstats.nbr_new_dsites.
    """
    supplier = models.ForeignKey(Supplier, related_name="stats")
    rating_yelp = models.IntegerField(default=0)
    rating_tripadvisor = models.IntegerField(default=0)
    nbr_new_dsites = models.IntegerField(default=0)
    dsites = models.ManyToManyField('dsites.DSite', blank=True, null=True, related_name='+')

    class Meta:
        verbose_name = _('Deal supplier statistics')
        verbose_name_plural = _('Deal suppliers statistics')
        app_label = 'suppliers'
        ordering = ['supplier', '-counter']

    def __unicode__(self):
        return "supplier: %s, counter: %d" % (self.supplier, self.counter)

    def save(self, **kwargs):
        current_stats = self.supplier.current_stats
        if current_stats is not None and self.id is None:
            self.counter = current_stats.counter + 1
            self.previous = self.supplier.current_stats
        super(SupplierStats, self).save(**kwargs)


@receiver(post_save, sender=SupplierStats)
def set_supplier_stats(sender, *args, **kwargs):
    """Signal handler to ensure that a new stats is always chosen as the
    current stats - automatically. It simplifies stuff greatly. Also
    stores previous revision for diff-purposes"""
    instance = kwargs['instance']
    created = kwargs['created']
    if created and instance.supplier:
        instance.supplier.current_stats = instance
        instance.supplier.save()
