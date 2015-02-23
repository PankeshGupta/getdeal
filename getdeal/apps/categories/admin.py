# -*- coding: utf-8 -*-
"""
Created on Sep 01, 2013
"""
from django.contrib import admin

from .models import (Category, SubCategory, CategoryMapping, SubCategoryMapping, CategoryStats)

admin.site.register((CategoryMapping, SubCategoryMapping, Category, SubCategory))


class CategoryStatsAdmin(admin.ModelAdmin):
    fields = ('category', 'nbr_rated_deals', 'nbr_positive_deals', 'nbr_negative_deals',
              'nbr_shared_deals', 'nbr_viewed_deals', 'nbr_wished_deals', 'nbr_bought_deals',
              'nbr_claimed_deals', 'nbr_buried_deals', 'avg_rating_deals', 'nbr_new_deals',
              'nbr_active_deals', 'nbr_subscribers', 'score',
              'created_on', 'counter', 'previous',)
    readonly_fields = ('created_on', 'counter', 'previous',)
    list_filter = ('category', 'created_on',)
    list_display = ('score', 'get_category',)

    def get_category(self, obj):
        return "%s" % obj.category

    get_category.short_description = 'category'


admin.site.register(CategoryStats, CategoryStatsAdmin)
