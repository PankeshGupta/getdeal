# -*- coding: utf-8 -*-
"""
Created on Nov 02, 2013
"""
from django.conf.urls import patterns, url

from .views import CustomRegistrationView
from .forms import RegistrationForm

urlpatterns = patterns('',
                       url(r'^register/$',
                           CustomRegistrationView.as_view(form_class=RegistrationForm),
                           name='registration_register'),
                       )
