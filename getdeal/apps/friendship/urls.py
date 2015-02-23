# -*- coding: utf-8 -*-
"""
Created on Sep 22, 2013
"""
from django.conf.urls import patterns, url

import api

urlpatterns = patterns('',
   url(r'^(?P<username>[\w.]+)/follow/$', api.FollowUser.as_view(), name='user-relationship'),
   url(r'^(?P<username>[\w.]+)/followers/$', api.FollowerList.as_view(), name='user-followers'),
   url(r'^(?P<username>[\w.]+)/following/$', api.FollowingList.as_view(), name='user-following'),
)
