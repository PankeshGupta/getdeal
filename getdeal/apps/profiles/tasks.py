# -*- coding: utf-8 -*-
"""
Created on Sep 22, 2013
"""
from celery.task import task

from django.db.models import Count

from apps.lists.models import RateList, ShareList, ViewList, WishList, WalletList, ClaimList
from apps.subscriptions.models import (DSiteSubscription, CategorySubscription,
                                       SubCategorySubscription, CitySubscription,
                                       SupplierSubscription)
from .models import Profile, RNewUserQueue, ProfileStats


@task()
def email_new_user(user_id):
    user_profile = Profile.objects.get(user__pk=user_id)
    user_profile.send_new_user_email()


@task()
def activate_next_user():
    RNewUserQueue.activate_next()


@task(ignore_result=True, queue='profiles')
def new_stats_task(profile):
    ProfileStats.objects.create(profile=profile)


@task(queue='profiles')
def count_rated_deals_task(profile, time_from):
    RateList.objects.filter(
        user=profile.user,
        created_on__gte=time_from).values_list(
            'rating').annotate(Count('id')).order_by()


@task(queue='profiles')
def count_shared_deals_task(profile, time_from):
    ShareList.objects.filter(
        user=profile.user,
        created_on__gte=time_from).count()


@task(queue='profiles')
def count_viewed_deals_task(profile, time_from):
    ViewList.objects.filter(
        user=profile.user,
        created_on__gte=time_from).count()


@task(queue='profiles')
def count_wished_deals_task(profile, time_from):
    WishList.objects.filter(
        user=profile.user,
        created_on__gte=time_from).count()


@task(queue='profiles')
def count_bought_deals_task(profile, time_from):
    WalletList.objects.filter(
        user=profile.user,
        created_on__gte=time_from).count()


@task(queue='profiles')
def count_claimed_deals_task(profile, time_from):
    ClaimList.objects.filter(
        user=profile.user,
        created_on__gte=time_from).count()


@task(queue='profiles')
def average_rating_deals_task(profile, time_from):
    #@ todo : implement average rating
    pass


@task(queue='profiles')
def count_subscribers_task(profile, time_from):
    DSiteSubscription.objects.filter(
        user=profile.user,
        created_on__gte=time_from).count()
    CategorySubscription.objects.filter(
        user=profile.user,
        created_on__gte=time_from).count()
    SubCategorySubscription.objects.filter(
        user=profile.user,
        created_on__gte=time_from).count()
    CitySubscription.objects.filter(
        user=profile.user,
        created_on__gte=time_from).count()
    SupplierSubscription.objects.filter(
        user=profile.user,
        created_on__gte=time_from).count()

@task(queue='profiles')
def count_active_subscribers_task(profile, time_from):
    DSiteSubscription.objects.filter(
        user=profile.user,
        created_on__gte=time_from,
        is_active=True).count()
    CategorySubscription.objects.filter(
        user=profile.user,
        created_on__gte=time_from,
        is_active=True).count()
    SubCategorySubscription.objects.filter(
        user=profile.user,
        created_on__gte=time_from,
        is_active=True).count()
    CitySubscription.objects.filter(
        user=profile.user,
        created_on__gte=time_from,
        is_active=True).count()
    SupplierSubscription.objects.filter(
        user=profile.user,
        created_on__gte=time_from,
        is_active=True).count()


@task(queue='profiles')
def calculate_score_task(time_from):
    # @todo : nbt shared deals
    pass
