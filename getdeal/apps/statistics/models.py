# -*- coding: utf-8 -*-
"""
Created on Sep 23, 2013
"""
from django.db import models


class StatsBase(models.Model):
    """
    An base stats class that defines important indicators to track
    (all this stats are bound to one object during one period)
        nbr_shared_deals: number of shared deals
        nbr_rated_deals: number of rated deals (all kind of rating)
        nbr_positive_deals: number of positive ratings
        nbr_negative_deals: number of negative ratings
        nbr_viewed_deals: number of viewed deals
        nbr_wished_deals: number of wished deals
        nbr_bought_deals: number of bought deals
        nbr_claimed_deals: number of claimed deals
        nbr_buried_deals: number of buried  deals (user click hide deal)
        avg_rating_deals: average rating of active deals
        nbr_new_deals : number of newly added deals
        nbr_active_deals: number of active deals
        nbr_subscribers: number of user subscribing to this object
        nbr_active_subscribers: number of active subscribers
        created_on: time of creation
        counter: number of this instance
        previous: link to previous stats
    """
    nbr_rated_deals = models.IntegerField(default=0)
    nbr_positive_deals = models.IntegerField(default=0)
    nbr_negative_deals = models.IntegerField(default=0)
    nbr_shared_deals = models.IntegerField(default=0)
    nbr_viewed_deals = models.IntegerField(default=0)
    nbr_wished_deals = models.IntegerField(default=0)
    nbr_bought_deals = models.IntegerField(default=0)
    nbr_claimed_deals = models.IntegerField(default=0)
    nbr_buried_deals = models.IntegerField(default=0)
    avg_rating_deals = models.FloatField(default=0.0)
    nbr_new_deals = models.IntegerField(default=0)
    nbr_active_deals = models.IntegerField(default=0)
    nbr_subscribers = models.IntegerField(default=0)
    nbr_active_subscribers = models.IntegerField(default=0)
    score = models.FloatField(default=0.0)
    created_on = models.DateTimeField(auto_now_add=True)
    counter = models.IntegerField(default=1, editable=False)
    previous = models.ForeignKey('self', blank=True, null=True, editable=False)

    class Meta:
        abstract = True
