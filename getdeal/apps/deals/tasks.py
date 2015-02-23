# -*- coding: utf-8 -*-
"""
Created on Oct 12, 2013
"""
from celery import task

from django.utils.timezone import now

from models import Deal, DealStats


@task(ignore_result=True, queue='deals')
def new_stats_task():
    for deal in Deal.objects.filter(ends_on__gte=now()):
        DealStats.objects.create(deal=deal)


@task(queue='deals')
def calculate_score_task(time_from):
    # @todo : nbt shared deals
    pass
