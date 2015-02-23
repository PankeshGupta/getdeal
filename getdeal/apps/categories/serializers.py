# -*- coding: utf-8 -*-
"""
Created on Dec 24, 2013
"""
from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')
        read_only_fields = ('name', 'slug')
