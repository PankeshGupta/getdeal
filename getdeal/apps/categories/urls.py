# -*- coding: utf-8 -*-
"""
Created on Sep 22, 2013
"""
from django.conf.urls import patterns, include, url
import api

urlpatterns = patterns('',
   url(r'^(?P<name>[\w.]+)/$', api.CategoryDetail.as_view(), name='category-detail'),
)
