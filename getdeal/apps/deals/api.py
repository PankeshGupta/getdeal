# -*- coding: utf-8 -*-
"""
Created on Aug 19, 2013
"""
from rest_framework import generics
from rest_framework import permissions

from .models import Deal
from .serializers import DealSerializer


class DealList(generics.ListAPIView):
    model = Deal
    serializer_class = DealSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        """
        This view should return a list of deals
        """
        queryset = self.model._default_manager.all()
        query = self.kwargs.get('city', None)
        if query is not None:
            queryset = queryset.filter(city__name=query)
        return queryset
