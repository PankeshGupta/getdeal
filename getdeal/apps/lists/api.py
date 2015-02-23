# -*- coding: utf-8 -*-
"""
Created on Oct 13, 2013
"""
from django.http import Http404

from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView

from apps.deals.models import Deal
from apps.friendship.models import Friendship
import apps.notifications.models as notification
from .models import (ShareList, update_nbr_shares, RateList, update_nbr_rates, WishList, update_nbr_wishes,
                     WalletList, update_nbr_buyers, ClaimList, update_nbr_claims, BuryList,
                     update_nebr_buries)


class ListView(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_object(self, pk):
        try:
            obj = Deal.objects.get(pk=pk)
            return obj
        except Deal.DoesNotExist:
            raise Http404


class RateView(ListView):
    def post(self, request, pk, *args, **kwargs):
        deal = self.get_object(pk)
        user = request.user
        try:
            action = request.POST['action']
        except KeyError:
            action = None
        if action == "upvote":
            rate_list, is_new = RateList.objects.get_or_create(deal=deal, user=user)
            positive_update, negative_update = rate_list.upvote()
            update_nbr_rates(deal, is_new, positive_update, negative_update)
            notification.send(Friendship.active.get_followers(user),
                              'new_like',
                              dict(like_user=user, like_object=deal))
            return Response({"action": "upvoted"}, status=status.HTTP_201_CREATED)
        if action == "downvote":
            rate_list, is_new = RateList.objects.get_or_create(deal=deal, user=user)
            positive_update, negative_update = rate_list.downvote()
            update_nbr_rates(deal, is_new, positive_update, negative_update)
            return Response({"action": "downvoted"}, status=status.HTTP_201_CREATED)
        return Response({"status": "failed"}, status=status.HTTP_400_BAD_REQUEST)

        #@todo : add review method


class ShareView(ListView):
    def post(self, request, pk, *args, **kwargs):
        deal = self.get_object(pk)
        user = request.user
        try:
            action = request.POST['action']
            platform = request.POST['platform']
        except KeyError:
            action = None
            platform = None
        if action == "share":
            share_list, _ = ShareList.objects.get_or_create(deal=deal, user=user)
            share_list.add_platforms(platform)
            update_nbr_shares(deal)
            return Response({"action": "shared"}, status=status.HTTP_201_CREATED)
        return Response({"status": "failed"}, status=status.HTTP_400_BAD_REQUEST)


class WishView(ListView):
    def post(self, request, pk, *args, **kwargs):
        deal = self.get_object(pk)
        user = request.user
        try:
            action = request.POST['action']
        except KeyError:
            action = None
        if action == "wish":
            wish_list, is_new = WishList.objects.get_or_create(deal=deal, user=user)
            is_changed = wish_list.add_to_list()
            update_nbr_wishes(deal, 1, is_changed or is_new)
            return Response({"action": "added to wish list"}, status=status.HTTP_201_CREATED)
        if action == "unwish":
            wish_list, is_new = WishList.objects.get_or_create(deal=deal, user=user)
            is_changed = wish_list.remove_from_list()
            update_nbr_wishes(deal, -1, is_changed or is_new)
            return Response({"action": "removed from wish list"}, status=status.HTTP_201_CREATED)
        return Response({"status": "failed"}, status=status.HTTP_400_BAD_REQUEST)


class WalletView(ListView):
    def post(self, request, pk, *args, **kwargs):
        deal = self.get_object(pk)
        user = request.user
        try:
            action = request.POST['action']
        except KeyError:
            action = None
        if action == "buy":
            wallet_list, is_new = WalletList.objects.get_or_create(deal=deal, user=user)
            is_changed = wallet_list.add_to_list()
            update_nbr_buyers(deal, 1, is_changed or is_new)
            return Response({"action": "added to wallet list"}, status=status.HTTP_201_CREATED)
        if action == "unbuy":
            wallet_list, is_new = WalletList.objects.get_or_create(deal=deal, user=user)
            is_changed = wallet_list.remove_from_list()
            update_nbr_buyers(deal, -1, is_changed or is_new)
            return Response({"action": "removed from wallet list"}, status=status.HTTP_201_CREATED)
        return Response({"status": "failed"}, status=status.HTTP_400_BAD_REQUEST)


class ClaimView(ListView):
    def post(self, request, pk, *args, **kwargs):
        deal = self.get_object(pk)
        user = request.user
        try:
            action = request.POST['action']
        except KeyError:
            action = None
        if action == "claim":
            claim_list, is_new = ClaimList.objects.get_or_create(deal=deal, user=user)
            is_changed = claim_list.add_to_list()
            update_nbr_claims(deal, 1, is_changed or is_new)
            return Response({"action": "added to claim list"}, status=status.HTTP_201_CREATED)
        if action == "unclaim":
            claim_list, is_new = ClaimList.objects.get_or_create(deal=deal, user=user)
            is_changed = claim_list.remove_from_list()
            update_nbr_claims(deal, -1, is_changed or is_new)
            return Response({"action": "removed from claim list"}, status=status.HTTP_201_CREATED)
        return Response({"status": "failed"}, status=status.HTTP_400_BAD_REQUEST)


class BuryView(ListView):
    def post(self, request, pk, *args, **kwargs):
        deal = self.get_object(pk)
        user = request.user
        try:
            action = request.POST['action']
        except KeyError:
            action = None
        if action == "bury":
            bury_list, is_new = BuryList.objects.get_or_create(deal=deal, user=user)
            is_changed = bury_list.add_to_list()
            update_nebr_buries(deal, 1, is_changed or is_new)
            return Response({"action": "added to bury list"}, status=status.HTTP_201_CREATED)
        if action == "unbury":
            bury_list, is_new = BuryList.objects.get_or_create(deal=deal, user=user)
            is_changed = bury_list.remove_from_list()
            update_nebr_buries(deal, -1, is_changed or is_new)
            return Response({"action": "removed from bury list"}, status=status.HTTP_201_CREATED)
        return Response({"status": "failed"}, status=status.HTTP_400_BAD_REQUEST)
