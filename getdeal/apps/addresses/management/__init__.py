# -*- coding: utf-8 -*-
"""
Created on Aug 23, 2013
"""
from django.db.models import signals

from apps.addresses.models import City, Country


def create_cities(sender, **kwargs):
    country, _ = Country.objects.get_or_create(name="Maroc")
    City.objects.get_or_create(name='Casablanca', slug='casablanca', country=country)
    City.objects.get_or_create(name='Rabat', slug='rabat', country=country)
    City.objects.get_or_create(name='Marrakech', slug='marrakech', country=country)
    City.objects.get_or_create(name='Tanger', slug='tanger', country=country)
    City.objects.get_or_create(name='Agadir', slug='agadir', country=country)
    City.objects.get_or_create(name='Fes', slug='fes', country=country)
    City.objects.get_or_create(name='Mohammedia', slug='mohammedia', country=country)

signals.post_syncdb.connect(create_cities, sender=City)
