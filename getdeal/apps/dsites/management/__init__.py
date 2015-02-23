# -*- coding: utf-8 -*-
"""
Created on Aug 29, 2013
"""
from django.db.models import signals

from apps.addresses.models import Address, City, CityMapping
from apps.categories.models import Category, CategoryMapping

from .models import DSite, DSiteStats


def create_dsites(sender, **kwargs):
    #mydeal
    dsite, _ = DSite.objects.get_or_create(name='mydeal', url='http://mydeal.ma', phone1='05 22 29 90 61',
                                           has_both_mappings=True, has_city_mapping=False, has_category_mapping=True,
                                           email='contact@mydeal.ma', has_validity=True, has_nbr_buyers=True)
    #stats
    DSiteStats.objects.create(dsite=dsite)
    #category mapping
    CategoryMapping.objects.get_or_create(dsite=dsite, site_category='restaurants-sorties',
                                          target_category=Category.objects.get(slug='restauration'))
    CategoryMapping.objects.get_or_create(dsite=dsite, site_category='beaute-bien-etre',
                                          target_category=Category.objects.get(slug='beaute-bien-etre'))
    CategoryMapping.objects.get_or_create(dsite=dsite, site_category='sport-loisirs',
                                          target_category=Category.objects.get(slug='sorties-loisirs'))
    CategoryMapping.objects.get_or_create(dsite=dsite, site_category='shopping-deco',
                                          target_category=Category.objects.get(slug='shopping-services'))
    CategoryMapping.objects.get_or_create(dsite=dsite, site_category='high-tech',
                                          target_category=Category.objects.get(slug='high-tech'))
    CategoryMapping.objects.get_or_create(dsite=dsite, site_category='voyages', all_cities=True,
                                          target_category=Category.objects.get(slug='voyages'))
    #city mapping
    CityMapping.objects.get_or_create(dsite=dsite, site_city='casablanca',
                                      target_city=City.objects.get(slug='casablanca'))
    CityMapping.objects.get_or_create(dsite=dsite, site_city='rabat',
                                      target_city=City.objects.get(slug='rabat'))
    CityMapping.objects.get_or_create(dsite=dsite, site_city='marrakech',
                                      target_city=City.objects.get(slug='marrakech'))
    CityMapping.objects.get_or_create(dsite=dsite, site_city='mohammedia',
                                      target_city=City.objects.get(slug='mohammedia'))
    CityMapping.objects.get_or_create(dsite=dsite, site_city='fes',
                                      target_city=City.objects.get(slug='fes'))
    CityMapping.objects.get_or_create(dsite=dsite, site_city='agadir',
                                      target_city=City.objects.get(slug='agadir'))
    CityMapping.objects.get_or_create(dsite=dsite, site_city='tanger',
                                      target_city=City.objects.get(slug='tanger'))
    #marocdeal
    dsite, _ = DSite.objects.get_or_create(name='marocdeal', url='http://marocdeal.com', phone1='06 61 91 92 44',
                                           has_both_mappings=True, has_city_mapping=False, has_category_mapping=True,
                                           email='info@marocdeal.com', has_validity=True, has_nbr_buyers=True)
    #stats
    DSiteStats.objects.create(dsite=dsite)
    #category mapping
    CategoryMapping.objects.get_or_create(dsite=dsite, site_category='gastronomie',
                                          target_category=Category.objects.get(slug='restauration'))
    CategoryMapping.objects.get_or_create(dsite=dsite, site_category='beaute',
                                          target_category=Category.objects.get(slug='beaute-bien-etre'))
    CategoryMapping.objects.get_or_create(dsite=dsite, site_category='bien-etre',
                                          target_category=Category.objects.get(slug='beaute-bien-etre'))
    CategoryMapping.objects.get_or_create(dsite=dsite, site_category='loisirs',
                                          target_category=Category.objects.get(slug='sorties-loisirs'))
    CategoryMapping.objects.get_or_create(dsite=dsite, site_category='services',
                                          target_category=Category.objects.get(slug='shopping-services'))
    CategoryMapping.objects.get_or_create(dsite=dsite, site_category='shopping',
                                          target_category=Category.objects.get(slug='shopping-services'))
    CategoryMapping.objects.get_or_create(dsite=dsite, site_category='high-tech',
                                          target_category=Category.objects.get(slug='high-tech'))
    CategoryMapping.objects.get_or_create(dsite=dsite, site_category='voyages', all_cities=True,
                                          target_category=Category.objects.get(slug='voyages'))
    #city mapping
    CityMapping.objects.get_or_create(dsite=dsite, site_city='casablanca',
                                      target_city=City.objects.get(slug='casablanca'))
    CityMapping.objects.get_or_create(dsite=dsite, site_city='rabat',
                                      target_city=City.objects.get(slug='rabat'))
    CityMapping.objects.get_or_create(dsite=dsite, site_city='marrakech',
                                      target_city=City.objects.get(slug='marrakech'))
    CityMapping.objects.get_or_create(dsite=dsite, site_city='mohammedia',
                                      target_city=City.objects.get(slug='mohammedia'))
    CityMapping.objects.get_or_create(dsite=dsite, site_city='agadir',
                                      target_city=City.objects.get(slug='agadir'))
    CityMapping.objects.get_or_create(dsite=dsite, site_city='tanger',
                                      target_city=City.objects.get(slug='tanger'))
    CityMapping.objects.get_or_create(dsite=dsite, site_city='fes',
                                      target_city=City.objects.get(slug='fes'))
    #dealexpress
    dsite, _ = DSite.objects.get_or_create(name='dealexpress', url='http://dealexpress.co', phone1='05 22 27 25 27',
                                           has_both_mappings=False, has_city_mapping=True, has_category_mapping=False,
                                           phone2='06 30 25 90 50', has_validity=True, has_nbr_buyers=True)
    #stats
    DSiteStats.objects.create(dsite=dsite)
    #category mapping
    CategoryMapping.objects.get_or_create(dsite=dsite, site_category='Gastronomie',
                                          target_category=Category.objects.get(slug='restauration'))
    CategoryMapping.objects.get_or_create(dsite=dsite, site_category='Beauté&Bien être',
                                          target_category=Category.objects.get(slug='beaute-bien-etre'))
    CategoryMapping.objects.get_or_create(dsite=dsite, site_category='Sport',
                                          target_category=Category.objects.get(slug='sorties-loisirs'))
    CategoryMapping.objects.get_or_create(dsite=dsite, site_category='Shopping',
                                          target_category=Category.objects.get(slug='shopping-services'))
    CategoryMapping.objects.get_or_create(dsite=dsite, site_category='Bijouterie',
                                          target_category=Category.objects.get(slug='shopping-services'))
    CategoryMapping.objects.get_or_create(dsite=dsite, site_category='Maison & Deco',
                                          target_category=Category.objects.get(slug='shopping-services'))
    CategoryMapping.objects.get_or_create(dsite=dsite, site_category='Hi-Tech',
                                          target_category=Category.objects.get(slug='high-tech'))
    CategoryMapping.objects.get_or_create(dsite=dsite, site_category='Voyages', all_cities=True,
                                          target_category=Category.objects.get(slug='voyages'))
    #city mapping
    CityMapping.objects.get_or_create(dsite=dsite, site_city='9',
                                      target_city=City.objects.get(slug='casablanca'))
    CityMapping.objects.get_or_create(dsite=dsite, site_city='7',
                                      target_city=City.objects.get(slug='rabat'))
    CityMapping.objects.get_or_create(dsite=dsite, site_city='8',
                                      target_city=City.objects.get(slug='marrakech'))
    CityMapping.objects.get_or_create(dsite=dsite, site_city='6',
                                      target_city=City.objects.get(slug='agadir'))
    CityMapping.objects.get_or_create(dsite=dsite, site_city='5',
                                      target_city=City.objects.get(slug='tanger'))
    CityMapping.objects.get_or_create(dsite=dsite, site_city='4',
                                      target_city=City.objects.get(slug='fes'))
    #hmizate
    dsite, _ = DSite.objects.get_or_create(name='hmizate', url='http://hmizate.ma', phone1='05 22 92 66 40',
                                           has_both_mappings=False, has_city_mapping=True, has_category_mapping=True,
                                           email='support@hmizate.ma', has_validity=True, has_nbr_buyers=True)
    #stats
    DSiteStats.objects.create(dsite=dsite)
    #category mapping
    CategoryMapping.objects.get_or_create(dsite=dsite, site_category='Restauration',
                                          target_category=Category.objects.get(slug='restauration'))
    CategoryMapping.objects.get_or_create(dsite=dsite, site_category='Beauté & Bien-être',
                                          target_category=Category.objects.get(slug='beaute-bien-etre'))
    CategoryMapping.objects.get_or_create(dsite=dsite, site_category='Loisirs',
                                          target_category=Category.objects.get(slug='sorties-loisirs'))
    CategoryMapping.objects.get_or_create(dsite=dsite, site_category='Services',
                                          target_category=Category.objects.get(slug='shopping-services'))
    CategoryMapping.objects.get_or_create(dsite=dsite, site_category='Auto-Moto',
                                          target_category=Category.objects.get(slug='shopping-services'))
    CategoryMapping.objects.get_or_create(dsite=dsite, site_category='Fashion',
                                          target_category=Category.objects.get(slug='shopping-services'))
    CategoryMapping.objects.get_or_create(dsite=dsite, site_category='hotels', all_cities=True,
                                          target_category=Category.objects.get(slug='voyages'))
    CategoryMapping.objects.get_or_create(dsite=dsite, site_category='shopping', all_cities=True,
                                          target_category=Category.objects.get(slug='shopping-services'))
    CategoryMapping.objects.get_or_create(dsite=dsite, site_category='hi-tech', all_cities=True,
                                          target_category=Category.objects.get(slug='shopping-services'))
    CategoryMapping.objects.get_or_create(dsite=dsite, site_category='vip', all_cities=True,
                                          target_category=Category.objects.get(slug='sorties-loisirs'))
    #city mapping
    CityMapping.objects.get_or_create(dsite=dsite, site_city='casablanca',
                                      target_city=City.objects.get(slug='casablanca'))
    CityMapping.objects.get_or_create(dsite=dsite, site_city='rabat',
                                      target_city=City.objects.get(slug='rabat'))
    CityMapping.objects.get_or_create(dsite=dsite, site_city='marrakech',
                                      target_city=City.objects.get(slug='marrakech'))
    CityMapping.objects.get_or_create(dsite=dsite, site_city='fes',
                                      target_city=City.objects.get(slug='fes'))
    CityMapping.objects.get_or_create(dsite=dsite, site_city='tanger',
                                      target_city=City.objects.get(slug='tanger'))
    CityMapping.objects.get_or_create(dsite=dsite, site_city='agadir',
                                      target_city=City.objects.get(slug='agadir'))
    #superdeal
    dsite, _ = DSite.objects.get_or_create(name='superdeal', url='http://superdeal.ma', phone1='05 22 36 00 88',
                                           has_both_mappings=True, has_city_mapping=False, has_category_mapping=True,
                                           email='info@superdeal.ma', has_validity=True, has_nbr_buyers=True)
    #stats
    DSiteStats.objects.create(dsite=dsite)
    #category mapping
    CategoryMapping.objects.get_or_create(dsite=dsite, site_category='patisserie-traiteur',
                                          target_category=Category.objects.get(slug='restauration'))
    CategoryMapping.objects.get_or_create(dsite=dsite, site_category='restaurant',
                                          target_category=Category.objects.get(slug='restauration'))
    CategoryMapping.objects.get_or_create(dsite=dsite, site_category='bien-etre',
                                          target_category=Category.objects.get(slug='beaute-bien-etre'))
    CategoryMapping.objects.get_or_create(dsite=dsite, site_category='beaute',
                                          target_category=Category.objects.get(slug='beaute-bien-etre'))
    CategoryMapping.objects.get_or_create(dsite=dsite, site_category='activites-loisirs',
                                          target_category=Category.objects.get(slug='sorties-loisirs'))
    CategoryMapping.objects.get_or_create(dsite=dsite, site_category='service',
                                          target_category=Category.objects.get(slug='shopping-services'))
    CategoryMapping.objects.get_or_create(dsite=dsite, site_category='voyages', all_cities=True,
                                          target_category=Category.objects.get(slug='voyages'))
    CategoryMapping.objects.get_or_create(dsite=dsite, site_category='shopping', all_cities=True,
                                          target_category=Category.objects.get(slug='shopping-services'))
    CategoryMapping.objects.get_or_create(dsite=dsite, site_category='hightech', all_cities=True,
                                          target_category=Category.objects.get(slug='high-tech'))
    CategoryMapping.objects.get_or_create(dsite=dsite, site_category='tickets', all_cities=True,
                                          target_category=Category.objects.get(slug='shopping-services'))
    #city mapping
    CityMapping.objects.get_or_create(dsite=dsite, site_city='casablanca',
                                      target_city=City.objects.get(slug='casablanca'))
    CityMapping.objects.get_or_create(dsite=dsite, site_city='rabat',
                                      target_city=City.objects.get(slug='rabat'))
    CityMapping.objects.get_or_create(dsite=dsite, site_city='marrakech',
                                      target_city=City.objects.get(slug='marrakech'))
    CityMapping.objects.get_or_create(dsite=dsite, site_city='fes',
                                      target_city=City.objects.get(slug='fes'))
    CityMapping.objects.get_or_create(dsite=dsite, site_city='tanger',
                                      target_city=City.objects.get(slug='tanger'))
    CityMapping.objects.get_or_create(dsite=dsite, site_city='agadir',
                                      target_city=City.objects.get(slug='agadir'))
    #dealin
    dealin_address, _ = Address.objects.get_or_create(address="19 rue de Strasbourg, Casablanca")
    dsite, _ = DSite.objects.get_or_create(name='dealin', url='http://dealin.ma', address1=dealin_address,
                                           phone1='06 61 29 60 16', email='admin@dealin.ma',
                                           has_both_mappings=True, has_city_mapping=False, has_category_mapping=True,
                                           has_validity=True, has_nbr_buyers=True)
    #stats
    DSiteStats.objects.create(dsite=dsite)
    #category mapping
    CategoryMapping.objects.get_or_create(dsite=dsite, site_category='BEAUTE-&-BIEN-êTRE-deal-1-categorie',
                                          target_category=Category.objects.get(slug='beaute-bien-etre'))
    CategoryMapping.objects.get_or_create(dsite=dsite, site_category='RESTAURATION-deal-2-categorie',
                                          target_category=Category.objects.get(slug='restauration'))
    CategoryMapping.objects.get_or_create(dsite=dsite, site_category='VOYAGES-&-LOISIRS-deal-3-categorie',
                                          all_cities=True,
                                          target_category=Category.objects.get(slug='voyages'))
    CategoryMapping.objects.get_or_create(dsite=dsite, site_category='SHOPPING-deal-4-categorie',
                                          target_category=Category.objects.get(slug='shopping-services'))
    CategoryMapping.objects.get_or_create(dsite=dsite, site_category='HIGH-TECH-deal-5-categorie', all_cities=True,
                                          target_category=Category.objects.get(slug='high-tech'))
    #city mapping
    CityMapping.objects.get_or_create(dsite=dsite, site_city='casablanca',
                                      target_city=City.objects.get(slug='casablanca'))
    #hotelsdeal
    dsite, _ = DSite.objects.get_or_create(name='hotelsdeal', url='http://hotelsdeal.ma', phone1='05 24 31 31 74',
                                           has_both_mappings=False, has_city_mapping=False, has_category_mapping=True,
                                           phone2='06 26 70 39 49', has_validity=True, has_nbr_buyers=True,
                                           is_active=False)
    #stats
    DSiteStats.objects.create(dsite=dsite)
    #jevoyage
    dsite, _ = DSite.objects.get_or_create(name='jevoyage', url='http://jevoyage.ma', phone1='05 22 20 08 93',
                                           has_both_mappings=False, has_city_mapping=False, has_category_mapping=True,
                                           email='contact@jevoyage.ma', is_active=False)
    #stats
    DSiteStats.objects.create(dsite=dsite)
    #groupon
    dsite, _ = DSite.objects.get_or_create(name='groupon', url='http://groupon.ma', phone1='05 22 49 66 57',
                                           has_both_mappings=False, has_city_mapping=False, has_category_mapping=True,
                                           email='membres@groupon.ma', has_validity=True, is_active=False)
    #stats
    DSiteStats.objects.create(dsite=dsite)
    #undeal
    dsite, _ = DSite.objects.get_or_create(name='undeal', url='http://undeal.ma', has_validity=True,
                                           has_both_mappings=True, has_city_mapping=False, has_category_mapping=True,
                                           has_nbr_buyers=True, is_active=False)
    #stats
    DSiteStats.objects.create(dsite=dsite)
    #@todo: add mapping of categories for each dsite


signals.post_syncdb.connect(create_dsites, sender=DSiteStats)
