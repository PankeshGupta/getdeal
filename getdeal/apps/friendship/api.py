# -*- coding: utf-8 -*-
"""
Created on Sep 22, 2013
"""
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import Http404

from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from apps.profiles.models import Profile
from apps.profiles.serializers import ProfileSerializer
from .models import Friendship, follow, unfollow


class FollowUser(APIView):
    """
    Get if user follow/unfollow a user, follow/unfollow user
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    lookup_field = 'username'

    def get_object(self, username):
        try:
            obj = User.objects.get(username=username)
            self.check_object_permissions(self.request, obj)
            return obj
        except User.DoesNotExist:
            raise Http404

    def get(self, request, username, format=None):
        """
        Return a current relationship between user and other user
        """
        user = self.get_object(username=username)
        if Friendship.active.is_follower(request.user, user):
            return Response({"action": "following"})
        return Response({"action": "unfollowing"})

    def post(self, request, username, format=None):
        to_user = self.get_object(username=username)
        from_user = request.user
        try:
            action = request.POST['action']
        except KeyError:
            action = None
        if action == "follow":
            if not Friendship.active.is_follower(from_user, to_user):
                friendship, _ = Friendship.objects.get_or_create(from_user=from_user, to_user=to_user)
                friendship.reactivate()
                follow(friendship)
            return Response({"action": "following"}, status=status.HTTP_201_CREATED)
        if action == "unfollow":
            if Friendship.active.is_follower(from_user, to_user):
                friendship, _ = Friendship.objects.get_or_create(from_user=from_user, to_user=to_user)
                friendship.block()
                unfollow(friendship)
            return Response({"action": "unfollowing"}, status=status.HTTP_201_CREATED)
        return Response({"status": "failed"}, status=status.HTTP_400_BAD_REQUEST)


class FollowerList(generics.ListAPIView):
    """
    List all followers for a user.
    """
    model = Profile
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    lookup_field = 'username'

    def get_queryset(self):
        username = self.kwargs.get('username', None)
        if username is not None:
            to_user = get_object_or_404(User, username=username)
            return Friendship.active.get_followers(to_user=to_user,
                                                   profile=True,
                                                   from_user_request=self.request.user)
        return []


class FollowingList(generics.ListAPIView):
    """
    List all followers for a user.
    """
    model = Profile
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    lookup_field = 'username'

    def get_queryset(self):
        username = self.kwargs.get('username', None)
        if username is not None:
            from_user = get_object_or_404(User, username=username)
            return Friendship.active.get_followed(from_user=from_user,
                                                  profile=True,
                                                  to_user_request=self.request.user)
        return []
