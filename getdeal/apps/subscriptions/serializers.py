# -*- coding: utf-8 -*-
"""
Created on Dec 27, 2013
"""
from rest_framework import serializers

from .models import CategorySubscription


class CategorySubscriptionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = CategorySubscription
        fields = ('is_active',)
