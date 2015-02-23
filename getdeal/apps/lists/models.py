# -*- coding: utf-8 -*-
"""
Created on Sep 24, 2013
"""
import json

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class List(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    nbr_updates = models.IntegerField(default=0)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.nbr_updates += 1
        super(List, self).save(**kwargs)


class ActivateList(List):
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def remove_from_list(self, commit=True):
        if not self.is_active:
            return False
        self.is_active = False
        if commit:
            self.save()
        return True

    def add_to_list(self, commit=True):
        if self.is_active:
            return False
        self.is_active = True
        if commit:
            self.save()
        return True


class RateList(List):
    NULL_VOTE = '0'
    UP_VOTE = '1'
    DOWN_VOTE = '2'

    RATING = (
        ('0', _('Null')),
        ('1', _('Up')),
        ('2', _('Down')),
    )

    deal = models.ForeignKey('deals.Deal', related_name='raters')
    user = models.ForeignKey(User, related_name='rated_deals')
    rating = models.CharField(max_length=1, default=NULL_VOTE, choices=RATING)
    review = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Rate list')
        verbose_name_plural = _('Rate lists')
        app_label = 'lists'
        unique_together = (('deal', 'user'),)

    def add_review(self, review='', commit=True):
        if review:
            self.review = review
            if commit:
                self.save()

    def remove_review(self, commit=True):
        self.review = ''
        self.is_active = False
        if commit:
            self.save()

    def nullvote(self, commit=True):
        """
        Check the current rating, and update with new one.
        Return the values by which we should increment/decrement nbr_positive/negative_deals in stats.
            Should follow this rule: positive_update, negative_update
        """
        if self.rating == self.NULL_VOTE:
            return 0, 0
        elif self.rating == self.UP_VOTE:
            self.rating = self.NULL_VOTE
            if commit:
                self.save()
            return -1, 0
        elif self.rating == self.DOWN_VOTE:
            self.rating = self.NULL_VOTE
            if commit:
                self.save()
            return 0, -1

    def upvote(self, commit=True):
        """
        Check the current rating, and update with new one.
        Return the values by which we should increment/decrement nbr_positive/negative_deals in stats.
            Should follow this rule: positive_update, negative_update
        """
        if self.rating == self.NULL_VOTE:
            self.rating = self.UP_VOTE
            if commit:
                self.save()
            return 1, 0
        elif self.rating == self.DOWN_VOTE:
            self.rating = self.UP_VOTE
            if commit:
                self.save()
            return 1, -1
        elif self.rating == self.UP_VOTE:
            self.rating = self.NULL_VOTE
            if commit:
                self.save()
            return -1, 0

    def downvote(self, commit=True):
        """
        Check the current rating, and update with new one.
        Return the values by which we should increment/decrement nbr_positive/negative_deals in stats.
            Should follow this rule: positive_update, negative_update
        """
        if self.rating == self.NULL_VOTE:
            self.rating = self.DOWN_VOTE
            if commit:
                self.save()
            return 0, 1
        elif self.rating == self.UP_VOTE:
            self.rating = self.DOWN_VOTE
            if commit:
                self.save()
            return -1, 1
        elif self.rating == self.DOWN_VOTE:
            self.rating = self.NULL_VOTE
            if commit:
                self.save()
            return 0, -1


def update_nbr_rates(deal, is_new, positive_update, negative_update):
    deal_stats = deal.current_stats
    if is_new:
        deal_stats.nbr_rates += 1
    deal_stats.nbr_positive_rates += positive_update
    deal_stats.nbr_negative_rates += negative_update
    deal_stats.save()


class ShareList(List):

    deal = models.ForeignKey('deals.Deal', related_name='shared_deals')
    user = models.ForeignKey(User, related_name='sharers')
    platforms = models.TextField(default='[]')

    class Meta:
        verbose_name = _('Share list')
        verbose_name_plural = _('Share lists')
        app_label = 'lists'
        unique_together = (('deal', 'user'),)

    def add_platforms(self, *args, **kwargs):
        platforms = json.loads(self.platforms)
        for p in args:
            if p not in platforms:
                platforms.append(p)
        self.platforms = json.dumps(platforms)
        if kwargs.get('commit', True):
            self.save()


def update_nbr_shares(deal):
    deal.current_stats.nbr_shares += 1
    deal.current_stats.save()


class ViewList(List):
    deal = models.ForeignKey('deals.Deal', related_name='viewed_deals')
    user = models.ForeignKey(User, related_name='viewers')
    is_redirected = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('View list')
        verbose_name_plural = _('View lists')
        app_label = 'lists'
        unique_together = (('deal', 'user'),)

    def redirect(self, commit=True):
        self.is_redirected = True
        if commit:
            self.save()


def update_nbr_views(deal):
    deal.current_stats.nbr_views += 1
    deal.current_stats.save()


class WishList(ActivateList):
    deal = models.ForeignKey('deals.Deal', related_name='wished_deals')
    user = models.ForeignKey(User, related_name='wishers')

    class Meta:
        verbose_name = _('Wish list')
        verbose_name_plural = _('Wish lists')
        app_label = 'lists'
        unique_together = (('deal', 'user'),)


def update_nbr_wishes(deal, nbr, is_changed):
    if is_changed:
        deal.current_stats.nbr_wishes += nbr
        deal.current_stats.save()


class WalletList(ActivateList):
    deal = models.ForeignKey('deals.Deal', related_name='bought_deals')
    user = models.ForeignKey(User, related_name='buyers')

    class Meta:
        verbose_name = _('Wallet list')
        verbose_name_plural = _('Wallet lists')
        app_label = 'lists'
        unique_together = (('deal', 'user'),)


def update_nbr_buyers(deal, nbr, is_changed):
    if is_changed:
        deal.current_stats.nbr_buyers += nbr
        deal.current_stats.save()


class ClaimList(ActivateList):
    deal = models.ForeignKey('deals.Deal', related_name='claimed_deals')
    user = models.ForeignKey(User, related_name='claimers')

    class Meta:
        verbose_name = _('Claim list')
        verbose_name_plural = _('Claim lists')
        app_label = 'lists'
        unique_together = (('deal', 'user'),)


def update_nbr_claims(deal, nbr, is_changed):
    if is_changed:
        deal.current_stats.nbr_claims += nbr
        deal.current_stats.save()


class BuryList(ActivateList):
    deal = models.ForeignKey('deals.Deal', related_name='buried_deals')
    user = models.ForeignKey(User, related_name='buries')

    class Meta:
        verbose_name = _('Bury list')
        verbose_name_plural = _('Bury lists')
        app_label = 'lists'
        unique_together = (('deal', 'user'),)


def update_nebr_buries(deal, nbr, is_changed):
    if is_changed:
        deal.current_stats.nbr_buries += nbr
        deal.current_stats.save()
