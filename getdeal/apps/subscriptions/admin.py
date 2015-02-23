# -*- coding: utf-8 -*-
"""
Created on Sep 25, 2013
"""
from django.contrib import admin
from .models import (CategorySubscription, SubCategorySubscription, CitySubscription,
                     SupplierSubscription, DSiteSubscription)

admin.site.register((CategorySubscription, SubCategorySubscription, CitySubscription, SupplierSubscription,
                     DSiteSubscription))
