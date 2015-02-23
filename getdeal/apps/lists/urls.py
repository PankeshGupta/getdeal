# -*- coding: utf-8 -*-
"""
Created on Nov 02, 2013
"""
from django.conf.urls import patterns, url

import api

urlpatterns = patterns('',
    url(r'^(?P<pk>[\w.]+)/rate/$', api.RateView.as_view(), name='deal-rate'),
    url(r'^(?P<pk>[\w.]+)/share/$', api.ShareView.as_view(), name='deal-share'),
    url(r'^(?P<pk>[\w.]+)/wish/$', api.WishView.as_view(), name='deal-wish'),
    url(r'^(?P<pk>[\w.]+)/wallet/$', api.WalletView.as_view(), name='deal-wallet'),
    url(r'^(?P<pk>[\w.]+)/claim/$', api.ClaimView.as_view(), name='deal-claim'),
    url(r'^(?P<pk>[\w.]+)/bury/$', api.BuryView.as_view(), name='deal-bury'),
)
