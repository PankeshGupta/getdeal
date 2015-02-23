# -*- coding: utf-8 -*-
"""
Created on Sep 22, 2013
"""
from django.contrib.auth.models import User
from django.http import Http404

from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.deals.models import Deal
from apps.deals.serializers import DealSerializer

from apps.friendship.models import Friendship
from apps.lists.models import RateList
from apps.subscriptions.models import CategorySubscription
from apps.subscriptions.serializers import CategorySubscriptionSerializer

from .models import Profile
from .serializers import UserSerializer, ProfileSerializer
from .permissions import IsProfileOwnerOrReadOnly, IsUserOwnerOrReadOnly


class UserList(generics.ListAPIView):
    model = User
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        """
        This view should return a list of
            if q, all users that contain q
            else, all users
        """
        queryset = self.model._default_manager.all()
        query = self.request.QUERY_PARAMS.get('q', None)
        query_eq = self.request.QUERY_PARAMS.get('eq', None)
        if query is not None:
            if query_eq:
                queryset = queryset.filter(username=query)
            else:
                queryset = queryset.filter(username__icontains=query)
        return queryset


class UserDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve, update or delete a user instance.
    """
    model = User
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsUserOwnerOrReadOnly)
    lookup_field = 'username'

    def pre_save(self, obj):
        pass


class ProfileList(generics.ListAPIView):
    model = Profile
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    lookup_field = 'username'

    def get_queryset(self):
        """
        This view should return a list of
            if q, all profiles that contain q
            else, all profiles
        """
        queryset = self.model._default_manager.all()
        query = self.request.QUERY_PARAMS.get('q', None)
        if query is not None:
            queryset = queryset.filter(user__username__icontains=query)
        return queryset


class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve, update or delete a profile instance.
    """
    model = Profile
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsProfileOwnerOrReadOnly)
    lookup_field = 'username'

    def get_object(self):
        try:
            username = self.kwargs.get('username', None)
            obj = self.model._default_manager.get(user__username=username)
            obj.set_following(Friendship.active.is_follower(self.request.user, obj))
            self.check_object_permissions(self.request, obj)
            return obj
        except Profile.DoesNotExist:
            raise Http404

    def pre_save(self, obj):
        pass


class UserCategorySubscriptionList(generics.ListAPIView):
    """
    List all Category Subscriptions for a user.
    """
    model = CategorySubscription
    serializer_class = CategorySubscriptionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def get_queryset(self):
        username = self.kwargs.get('username', None)
        if username is not None:
            return CategorySubscription.objects.filter(author__username=username)
        return []


class FavoritesList(APIView):
    """
    List all favorites deals
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_object(self, username):
        try:
            obj = User.objects.get(username=username)
            self.check_object_permissions(self.request, obj)
            return obj
        except User.DoesNotExist:
            raise Http404

    def get(self, request, username, format=None):
        user = self.get_object(username)
        favorites = DealSerializer(Deal.objects.filter(pk__in=user.rated_deals.filter(rating=RateList.UP_VOTE).values_list('deal')))
        return Response(favorites.data)
