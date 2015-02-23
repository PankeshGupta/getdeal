# -*- coding: utf-8 -*-
"""
Created on Aug 23, 2013
"""
from rest_framework import generics
from rest_framework import permissions

from .models import Category
from .serializers import CategorySerializer


class CategoryDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve, update or delete a category instance.
    """
    model = Category
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAdminUser,)

    def pre_save(self, obj):
        pass
