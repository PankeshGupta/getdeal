# -*- coding: utf-8 -*-
"""
Created on Sep 01, 2013
"""
from django.contrib import admin

from apps.suppliers.models import Supplier, SupplierStats


class SupplierAdmin(admin.ModelAdmin):
    fields = ('slug', 'name', 'address1', 'address2', 'phone1', 'phone2', 'phone3',
              'fax', 'email', 'info', 'current_stats',)
    list_filter = ('name',)
    list_display = ('name', )
    list_display_links = ('name',)


admin.site.register(Supplier, SupplierAdmin)


class SupplierStatsAdmin(admin.ModelAdmin):
    fields = ('supplier', 'nbr_rated_deals', 'nbr_positive_deals', 'nbr_negative_deals',
              'nbr_shared_deals', 'nbr_viewed_deals', 'nbr_wished_deals', 'nbr_bought_deals',
              'nbr_claimed_deals', 'nbr_buried_deals', 'avg_rating_deals', 'nbr_new_deals',
              'nbr_active_deals', 'nbr_subscribers', 'score',
              'created_on', 'counter', 'previous',)
    readonly_fields = ('created_on', 'counter', 'previous',)
    list_filter = ('supplier', 'created_on',)
    list_display = ('score', 'get_supplier',)

    def get_supplier(self, obj):
        return "%s" % obj.supplier

    get_supplier.short_description = 'supplier'


admin.site.register(SupplierStats, SupplierStatsAdmin)
