# -*- coding: utf-8 -*-
"""
Created on Dec 24, 2013
"""
from rest_framework import serializers

from .models import City


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('name',)
        read_only_fields = ('name',)
