# -*- coding: utf-8 -*-
"""
Created on Oct 12, 2013
"""
from celery.task import task

from django.db.models import Count

from apps.deals.models import Deal
from apps.lists.models import RateList, ShareList, ViewList, WishList, WalletList, ClaimList
from apps.subscriptions.models import SupplierSubscription
from .models import SupplierStats


@task(ignore_result=True, queue='supplier')
def new_stats_task(supplier):
    SupplierStats.objects.create(supplier=supplier)


@task(queue='supplier')
def count_new_deals_task(supplier, time_from):
    Deal.objects.filter(supplier=supplier, created_on__gte=time_from).count()


@task(queue='supplier')
def count_active_deals_task(supplier, time_from):
    Deal.objects.filter(supplier=supplier, ends_on__gte=time_from).count()


@task(queue='supplier')
def count_rated_deals_task(supplier, time_from):
    RateList.objects.filter(
        deal__supplier=supplier,
        created_on__gte=time_from).values_list(
            'rating').annotate(Count('id')).order_by()


@task(queue='supplier')
def count_shared_deals_task(supplier, time_from):
    ShareList.objects.filter(
        deal__supplier=supplier,
        created_on__gte=time_from).count()


@task(queue='supplier')
def count_viewed_deals_task(supplier, time_from):
    ViewList.objects.filter(
        deal__supplier=supplier,
        created_on__gte=time_from).count()


@task(queue='supplier')
def count_wished_deals_task(supplier, time_from):
    WishList.objects.filter(
        deal__supplier=supplier,
        created_on__gte=time_from).count()


@task(queue='supplier')
def count_bought_deals_task(supplier, time_from):
    WalletList.objects.filter(
        deal__supplier=supplier,
        created_on__gte=time_from).count()


@task(queue='supplier')
def count_claimed_deals_task(supplier, time_from):
    ClaimList.objects.filter(
        deal__supplier=supplier,
        created_on__gte=time_from).count()


@task(queue='supplier')
def average_rating_deals_task(supplier, time_from):
    #@ todo : implement average rating
    pass


@task(queue='supplier')
def count_subscribers_task(supplier, time_from):
    SupplierSubscription.objects.filter(
        deal__supplier=supplier,
        created_on__gte=time_from).count()

@task(queue='supplier')
def count_active_subscribers_task(supplier, time_from):
    SupplierSubscription.objects.filter(
        deal__supplier=supplier,
        created_on__gte=time_from,
        is_active=True).count()

@task(queue='supplier')
def calculate_score_task(time_from):
    # @todo : nbt shared deals
    pass
