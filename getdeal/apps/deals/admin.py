# -*- coding: utf-8 -*-
"""
Created on Sep 01, 2013
"""
from django.contrib import admin

from models import Deal, DealStats


class DealAdmin(admin.ModelAdmin):
    fields = ('title', 'url', 'description1', 'description2',
              'sell_price', 'initial_price', 'saving', 'discount', 'is_valid',
              'is_active', 'ends_on', 'validity', 'created_on', 'updated_on', 'image', 'thumbnail',
              'dsite', 'supplier', 'city', 'category', 'subcategory', 'current_stats',)
    readonly_fields = ('created_on', 'updated_on', 'thumbnail',)
    list_filter = ('is_valid', 'is_active', 'dsite', 'city', 'category', 'created_on', 'ends_on')
    list_display = ('title', 'is_valid', 'is_active', 'get_dsite', )
    list_display_links = ('title',)

    def get_dsite(self, obj):
        return "%s" % obj.dsite

    get_dsite.short_description = 'dsite'


admin.site.register(Deal, DealAdmin)


class DealStatsAdmin(admin.ModelAdmin):
    fields = ('deal', 'score', 'nbr_rates', 'nbr_positive_rates', 'nbr_negative_rates',
              'nbr_shares', 'nbr_views', 'nbr_wishes', 'nbr_buyers', 'nbr_claims', 'nbr_buries',
              'created_on', 'counter', 'previous',)
    readonly_fields = ('created_on', 'counter', 'previous',)
    list_filter = ('created_on',)
    list_display = ('get_deal_pk', 'counter', 'score',)

    def get_deal_pk(self, obj):
        return "%s" % obj.deal.pk

    get_deal_pk.short_description = 'deal_pk'

admin.site.register(DealStats, DealStatsAdmin)
