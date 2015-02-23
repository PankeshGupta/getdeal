# -*- coding: utf-8 -*-
"""
Created on Aug 23, 2013
"""
from rest_framework import generics
from rest_framework import permissions

from apps.addresses.models import City
from apps.addresses.serializers import CitySerializer


class CityDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve, update or delete a city instance.
    """
    model = City
    serializer_class = CitySerializer
    permission_classes = (permissions.IsAdminUser,)

    def pre_save(self, obj):
        pass
