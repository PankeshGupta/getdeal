# -*- coding: utf-8 -*-
"""
Created on Oct 12, 2013
"""
from celery import task

from django.db.models import Count

from apps.deals.models import Deal
from apps.lists.models import RateList, ShareList, ViewList, WishList, WalletList, ClaimList
from apps.subscriptions.models import CitySubscription
from .models import CityStats


@task(ignore_result=True, queue='cities')
def new_stats_task(city):
    CityStats.objects.create(city=city)


@task(queue='cities')
def count_new_deals_task(city, time_from):
    Deal.objects.filter(city=city, created_on__gte=time_from).count()


@task(queue='cities')
def count_active_deals_task(city, time_from):
    Deal.objects.filter(city=city, ends_on__gte=time_from).count()


@task(queue='cities')
def count_rated_deals_task(city, time_from):
    RateList.objects.filter(
        deal__city=city,
        created_on__gte=time_from).values_list(
            'rating').annotate(Count('id')).order_by()


@task(queue='cities')
def count_shared_deals_task(city, time_from):
    ShareList.objects.filter(
        deal__city=city,
        created_on__gte=time_from).count()


@task(queue='cities')
def count_viewed_deals_task(city, time_from):
    ViewList.objects.filter(
        deal__city=city,
        created_on__gte=time_from).count()


@task(queue='cities')
def count_wished_deals_task(city, time_from):
    WishList.objects.filter(
        deal__city=city,
        created_on__gte=time_from).count()


@task(queue='cities')
def count_bought_deals_task(city, time_from):
    WalletList.objects.filter(
        deal__city=city,
        created_on__gte=time_from).count()


@task(queue='cities')
def count_claimed_deals_task(city, time_from):
    ClaimList.objects.filter(
        deal__city=city,
        created_on__gte=time_from).count()


@task(queue='cities')
def average_rating_deals_task(city, time_from):
    #@ todo : implement average rating
    pass


@task(queue='cities')
def count_subscribers_task(city, time_from):
    CitySubscription.objects.filter(
        deal__city=city,
        created_on__gte=time_from).count()

@task(queue='cities')
def count_active_subscribers_task(city, time_from):
    CitySubscription.objects.filter(
        deal__city=city,
        created_on__gte=time_from,
        is_active=True).count()

@task(queue='cities')
def calculate_score_task(time_from):
    # @todo : nbt shared deals
    pass
