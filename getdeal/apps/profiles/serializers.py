# -*- coding: utf-8 -*-
"""
Created on Sep 22, 2013
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from apps.profiles.models import Profile, ProfileStats


class UserSerializer(serializers.HyperlinkedModelSerializer):
    api_url = serializers.SerializerMethodField('get_api_url')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'api_url')
        lookup_field = 'username'

    def get_api_url(self, obj):
        return "#/user/%s" % obj.username


class ProfileStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileStats
        fields = ('nbr_following', 'nbr_followers')
        read_only_fields = ('nbr_following', 'nbr_followers')


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)
    current_stats = ProfileStatsSerializer(read_only=True)
    following = serializers.CharField(source='get_following', read_only=True)

    class Meta:
        model = Profile
        fields = ('user', 'location', 'gender', 'current_stats', 'following')
        lookup_field = 'username'
