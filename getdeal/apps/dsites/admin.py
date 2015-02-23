# -*- coding: utf-8 -*-
"""
Created on Sep 01, 2013
"""
from django.contrib import admin

from .models import DSite, DSiteStats, CityDistribution, CategoryDistribution, SupplierDistribution


class DSiteAdmin(admin.ModelAdmin):
    fields = ('name', 'url', 'address1', 'address2', 'phone1', 'phone2', 'phone3', 'has_both_mappings',
              'has_city_mapping', 'has_category_mapping', 'fax', 'email', 'has_validity', 'has_nbr_buyers',
              'has_sub_categories', 'is_active', 'current_stats',)
    list_filter = ('name', 'is_active', 'has_validity', 'has_nbr_buyers', 'has_sub_categories')
    list_display = ('name', 'url', 'is_active')
    list_display_links = ('name',)


admin.site.register(DSite, DSiteAdmin)


class DSiteStatsAdmin(admin.ModelAdmin):
    fields = ('dsite', 'score', 'nbr_new_deals', 'nbr_active_deals',
              'nbr_likes', 'avg_rating_deals', 'avg_quality_suppliers',
              'created_on', 'counter', 'previous',)
    readonly_fields = ('created_on', 'counter', 'previous',)
    list_filter = ('dsite', 'created_on',)
    list_display = ('score', 'get_dsite',)

    def get_dsite(self, obj):
        return "%s" % obj.dsite

    get_dsite.short_description = 'dsite'


admin.site.register(DSiteStats, DSiteStatsAdmin)


class CityDistributionAdmin(admin.ModelAdmin):
    fields = ('stats', 'city', 'nbr_deals',)
    list_filter = ('stats__dsite', 'stats__counter', 'city',)
    list_display = ('get_dsite', 'counter', 'city', 'nbr_deals',)

    def counter(self, obj):
        return "%d" % obj.stats.counter

    def get_dsite(self, obj):
        return "%s" % obj.stats.dsite

    get_dsite.short_description = 'dsite'

admin.site.register(CityDistribution, CityDistributionAdmin)


class CategoryDistributionAdmin(admin.ModelAdmin):
    fields = ('stats', 'category', 'nbr_deals',)
    list_filter = ('stats__dsite', 'stats__counter', 'category',)
    list_display = ('get_dsite', 'counter', 'category', 'nbr_deals',)

    def counter(self, obj):
        return "%d" % obj.stats.counter

    def get_dsite(self, obj):
        return "%s" % obj.stats.dsite

    get_dsite.short_description = 'dsite'

admin.site.register(CategoryDistribution, CategoryDistributionAdmin)


class SupplierDistributionAdmin(admin.ModelAdmin):
    fields = ('stats', 'supplier', 'nbr_deals', 'is_new',)
    list_filter = ('stats__dsite', 'stats__counter', 'supplier', 'is_new',)
    list_display = ('get_dsite', 'counter', 'supplier', 'is_new', 'nbr_deals',)

    def counter(self, obj):
        return "%d" % obj.stats.counter

    def get_dsite(self, obj):
        return "%s" % obj.stats.dsite

    get_dsite.short_description = 'dsite'

admin.site.register(SupplierDistribution, SupplierDistributionAdmin)
