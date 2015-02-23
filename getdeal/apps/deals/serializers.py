# -*- coding: utf-8 -*-
"""
Created on Sep 22, 2013
"""
from rest_framework import serializers

from apps.addresses.serializers import CitySerializer
from apps.categories.serializers import CategorySerializer
from .models import DealStats, Deal


class DealStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealStats
        fields = ('nbr_positive_rates', 'nbr_negative_rates', 'nbr_views',
                  'nbr_buyers', 'counter')
        read_only_fields = ('nbr_positive_rates', 'nbr_negative_rates', 'nbr_views',
                            'nbr_buyers', 'counter')


class DealSerializer(serializers.HyperlinkedModelSerializer):
    current_stats = DealStatsSerializer(read_only=True)
    city = CitySerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    ends_on = serializers.SerializerMethodField('format_end_date')
    created_on = serializers.SerializerMethodField('format_start_date')

    class Meta:
        model = Deal
        fields = ('url', 'title', 'sell_price', 'initial_price', 'discount', 'saving',
                  'city', 'category', 'current_stats', 'created_on', 'ends_on')

    def format_start_date(self, obj):
        return obj.created_on.strftime('%Y-%m-%d-%H-%M-%S')

    def format_end_date(self, obj):
        return obj.ends_on.strftime('%Y-%m-%d-%H-%M-%S')
