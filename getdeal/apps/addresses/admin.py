# -*- coding: utf-8 -*-
"""
Created on Sep 01, 2013
"""
from django.contrib import admin

from .models import Address, City, Country, CityMapping, CityStats


class AddressAdmin(admin.ModelAdmin):
    list_display = ['address', 'computed_address', 'latitude', 'longitude', 'geocode_error']
    list_filter = ['geocode_error']
    search_fields = ['address']


admin.site.register(Address, AddressAdmin)
admin.site.register((City, Country, CityMapping))


class CityStatsAdmin(admin.ModelAdmin):
    fields = ('city', 'nbr_rated_deals', 'nbr_positive_deals', 'nbr_negative_deals',
              'nbr_shared_deals', 'nbr_viewed_deals', 'nbr_wished_deals', 'nbr_bought_deals',
              'nbr_claimed_deals', 'nbr_buried_deals', 'avg_rating_deals', 'nbr_new_deals',
              'nbr_active_deals', 'nbr_subscribers', 'score',
              'created_on', 'counter', 'previous',)
    readonly_fields = ('created_on', 'counter', 'previous',)
    list_filter = ('city', 'created_on',)
    list_display = ('score', 'get_city',)

    def get_city(self, obj):
        return "%s" % obj.city

    get_city.short_description = 'city'


admin.site.register(CityStats, CityStatsAdmin)
