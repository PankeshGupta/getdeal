# -*- coding: utf-8 -*-
"""
Created on Sep 25, 2013
"""
from django.contrib import admin
from .models import RateList, ShareList, ViewList, WishList, WalletList, ClaimList, BuryList

admin.site.register((RateList, ShareList, ViewList, WishList, WalletList, ClaimList, BuryList))
