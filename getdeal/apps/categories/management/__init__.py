# -*- coding: utf-8 -*-
"""
Created on Aug 23, 2013
"""
from django.utils.translation import ugettext_noop as _
from django.db.models import signals

from apps.categories.models import Category


def create_categories(sender, **kwargs):
    #internal categories
    Category.objects.get_or_create(name=_(u'Beauté & Bien-être'))
    Category.objects.get_or_create(name=_(u'Restauration'))
    Category.objects.get_or_create(name=_(u'Sorties & Loisirs'))
    Category.objects.get_or_create(name=_(u'Shopping & Services'))
    Category.objects.get_or_create(name=_(u'High Tech'))
    Category.objects.get_or_create(name=_(u'Voyages'))
    Category.objects.get_or_create(name=_(u'Autres'))

signals.post_syncdb.connect(create_categories, sender=Category)
