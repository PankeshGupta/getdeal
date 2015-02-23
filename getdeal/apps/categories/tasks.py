# -*- coding: utf-8 -*-
"""
Created on Oct 12, 2013
"""
from celery import task

from django.db.models import Count

from apps.deals.models import Deal
from apps.lists.models import RateList, ShareList, ViewList, WishList, WalletList, ClaimList
from apps.subscriptions.models import CategorySubscription, SubCategorySubscription
from .models import CategoryStats, SubCategoryStats


@task(ignore_result=True, queue='categories')
def new_category_stats_task(category, sub=False):
    if sub:
        SubCategoryStats.objects.create(subcategory=category)
    else:
        CategoryStats.objects.create(category=category)


@task(queue='categories')
def count_new_deals_task(category, time_from, sub=False):
    if sub:
        Deal.objects.filter(subcategory=category, created_on__gte=time_from).count()
    else:
        Deal.objects.filter(category=category, created_on__gte=time_from).count()


@task(queue='categories')
def count_active_deals_task(category, time_from, sub=False):
    if sub:
        Deal.objects.filter(subcategory=category, ends_on__gte=time_from).count()
    else:
        Deal.objects.filter(category=category, ends_on__gte=time_from).count()


@task(queue='categories')
def count_rated_deals_task(category, time_from, sub=False):
    if sub:
        RateList.objects.filter(
            deal__subcategory=category,
            created_on__gte=time_from).values_list(
                'rating').annotate(Count('id')).order_by()
    else:
        RateList.objects.filter(
            deal__category=category,
            created_on__gte=time_from).values_list(
                'rating').annotate(Count('id')).order_by()


@task(queue='categories')
def count_shared_deals_task(category, time_from, sub=False):
    if sub:
        ShareList.objects.filter(
            deal__subcategory=category,
            created_on__gte=time_from).count()
    else:
        ShareList.objects.filter(
            deal__category=category,
            created_on__gte=time_from).count()


@task(queue='categories')
def count_viewed_deals_task(category, time_from, sub=False):
    if sub:
        ViewList.objects.filter(
            deal__subcategory=category,
            created_on__gte=time_from).count()
    else:
        ViewList.objects.filter(
            deal__category=category,
            created_on__gte=time_from).count()


@task(queue='categories')
def count_wished_deals_task(category, time_from, sub=False):
    if sub:
        WishList.objects.filter(
            deal__subcategory=category,
            created_on__gte=time_from).count()
    else:
        WishList.objects.filter(
            deal__category=category,
            created_on__gte=time_from).count()


@task(queue='categories')
def count_bought_deals_task(category, time_from, sub=False):
    if sub:
        WalletList.objects.filter(
            deal__subcategory=category,
            created_on__gte=time_from).count()
    else:
        WalletList.objects.filter(
            deal__category=category,
            created_on__gte=time_from).count()


@task(queue='categories')
def count_claimed_deals_task(category, time_from, sub=False):
    if sub:
        ClaimList.objects.filter(
            deal__subcategory=category,
            created_on__gte=time_from).count()
    else:
        ClaimList.objects.filter(
            deal__category=category,
            created_on__gte=time_from).count()


@task(queue='categories')
def average_rating_deals_task(category, time_from, sub=False):
    #@ todo : implement average rating
    pass


@task(queue='categories')
def count_subscribers_task(category, time_from, sub=False):
    if sub:
        SubCategorySubscription.objects.filter(
            deal__subcategory=category,
            created_on__gte=time_from).count()
    else:
        CategorySubscription.objects.filter(
            deal__category=category,
            created_on__gte=time_from).count()


@task(queue='categories')
def count_active_subscribers_task(category, time_from, sub=False):
    if sub:
        SubCategorySubscription.objects.filter(
            deal__subcategory=category,
            created_on__gte=time_from,
            is_active=True).count()
    else:
        CategorySubscription.objects.filter(
            deal__category=category,
            created_on__gte=time_from,
            is_active=True).count()


@task(queue='categories')
def calculate_score_task(time_from, sub=False):
    # @todo : nbt shared deals
    pass
