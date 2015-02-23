# -*- coding: utf-8 -*-
"""
Created on Sep 22, 2013
"""
from django.conf.urls import patterns, include, url
import api
import views


urlpatterns = patterns('',
    url(r'^(?P<username>[\w.]+)/$', views.ProfileView.as_view(), name='profile-view'),
    url(r'^(?P<username>[\w.]+)/rates/$', views.ProfileRatesView.as_view(), name='profile-rates'),
    url(r'^edit/$', views.EditProfileView.as_view(), name='profile-edit'),
    url(r'^changepassword/$', views.ChangePasswordView.as_view(), name='password-edit'),
    url(r'^cities/$', views.CitiesManagementView.as_view(), name='city-preferences'),
    url(r'^newsletter/$', views.NewsletterPreferencesView.as_view(), name='newsletter-preferences'),
)

# api
urlpatterns += patterns('',
    url(r'^p/$', api.ProfileList.as_view(), name='profile-list'),
    url(r'^p/(?P<username>[\w.]+)/$', api.ProfileDetail.as_view(), name='profile-detail'),
    url(r'^$', api.UserList.as_view(), name='user-list'),
    url(r'^(?P<username>[\w.]+)/$', api.UserDetail.as_view(), name='user-detail'),
    url(r'^(?P<username>[\w.]+)/categories-subscriptions/$', api.UserCategorySubscriptionList.as_view(), name='user-categories-subscriptions'),
    url(r'^(?P<username>[\w.]+)/favorites/$', api.FavoritesList.as_view(), name='user-favorites'),
)
