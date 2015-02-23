# -*- coding: utf-8 -*-
"""
Created on Sep 22, 2013
"""
from django.contrib import admin

from .models import Profile, ProfileStats, Steps, Preferences

admin.site.register((Profile, ProfileStats, Steps, Preferences))
