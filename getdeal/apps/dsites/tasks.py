# -*- coding: utf-8 -*-
"""
Created on Oct 12, 2013
"""
from celery import task

from django.db.models import Count

from apps.deals.models import Deal
from apps.lists.models import RateList, ShareList, ViewList, WishList, WalletList, ClaimList
from apps.subscriptions.models import DSiteSubscription
from .models import DSiteStats


@task(ignore_result=True, queue='dsites')
def new_stats_task(dsite):
    DSiteStats.objects.create(dsite=dsite)


@task(queue='dsites')
def count_new_deals_task(dsite, time_from):
    Deal.objects.filter(dsite=dsite, created_on__gte=time_from).count()


@task(queue='dsites')
def count_active_deals_task(dsite, time_from):
    Deal.objects.filter(dsite=dsite, ends_on__gte=time_from).count()


@task(queue='dsites')
def count_rated_deals_task(dsite, time_from):
    RateList.objects.filter(
        deal__dsite=dsite,
        created_on__gte=time_from).values_list(
            'rating').annotate(Count('id')).order_by()


@task(queue='dsites')
def count_shared_deals_task(dsite, time_from):
    ShareList.objects.filter(
        deal__dsite=dsite,
        created_on__gte=time_from).count()


@task(queue='dsites')
def count_viewed_deals_task(dsite, time_from):
    ViewList.objects.filter(
        deal__dsite=dsite,
        created_on__gte=time_from).count()


@task(queue='dsites')
def count_wished_deals_task(dsite, time_from):
    WishList.objects.filter(
        deal__dsite=dsite,
        created_on__gte=time_from).count()


@task(queue='dsites')
def count_bought_deals_task(dsite, time_from):
    WalletList.objects.filter(
        deal__dsite=dsite,
        created_on__gte=time_from).count()


@task(queue='dsites')
def count_claimed_deals_task(dsite, time_from):
    ClaimList.objects.filter(
        deal__dsite=dsite,
        created_on__gte=time_from).count()


@task(queue='dsites')
def average_rating_deals_task(dsite, time_from):
    #@ todo : implement average rating
    pass


@task(queue='dsites')
def count_subscribers_task(dsite, time_from):
    DSiteSubscription.objects.filter(
        deal__dsite=dsite,
        created_on__gte=time_from).count()

@task(queue='dsites')
def count_active_subscribers_task(dsite, time_from):
    DSiteSubscription.objects.filter(
        deal__dsite=dsite,
        created_on__gte=time_from,
        is_active=True).count()

@task(queue='dsites')
def calculate_score_task(time_from):
    # @todo : nbt shared deals
    pass
