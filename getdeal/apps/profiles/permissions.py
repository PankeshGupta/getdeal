# -*- coding: utf-8 -*-
"""
Created on Sep 22, 2013
"""
from rest_framework import permissions


class IsUserOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the profile
        return obj == request.user


class IsProfileOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):        
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:            
            return True

        # Write permissions are only allowed to the owner of the profile
        return obj.user == request.user
