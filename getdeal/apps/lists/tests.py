# -*- coding: utf-8 -*-
"""
Created on Sep 24, 2013
"""
from model_mommy import mommy

from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.test import TestCase


from apps.deals.models import Deal
from .models import RateList, ShareList, ViewList, WishList, WalletList, ClaimList, BuryList


class ListTest(TestCase):
    def test_list_creation(self):
        list = mommy.prepare(RateList)
        self.assertTrue(isinstance(list, RateList))
        list = mommy.prepare(ShareList)
        self.assertTrue(isinstance(list, ShareList))
        list = mommy.prepare(ViewList)
        self.assertTrue(isinstance(list, ViewList))
        list = mommy.prepare(WishList)
        self.assertTrue(isinstance(list, WishList))
        list = mommy.prepare(WalletList)
        self.assertTrue(isinstance(list, WalletList))
        list = mommy.prepare(ClaimList)
        self.assertTrue(isinstance(list, ClaimList))
        list = mommy.prepare(BuryList)
        self.assertTrue(isinstance(list, BuryList))

    def test_integrity(self):
        user = mommy.make(User)
        deal = mommy.make(Deal)
        integrity_error = False
        try:
            mommy.make(RateList, _quantity=3, user=user, deal=deal)
        except IntegrityError:
            integrity_error = True
        self.assertTrue(integrity_error)
        integrity_error = False
        try:
            mommy.make(ShareList, _quantity=3, user=user, deal=deal)
        except IntegrityError:
            integrity_error = True
        self.assertTrue(integrity_error)
        integrity_error = False
        try:
            mommy.make(ViewList, _quantity=3, user=user, deal=deal)
        except IntegrityError:
            integrity_error = True
        self.assertTrue(integrity_error)
        integrity_error = False
        try:
            mommy.make(WishList, _quantity=3, user=user, deal=deal)
        except IntegrityError:
            integrity_error = True
        self.assertTrue(integrity_error)
        integrity_error = False
        try:
            mommy.make(WalletList, _quantity=3, user=user, deal=deal)
        except IntegrityError:
            integrity_error = True
        self.assertTrue(integrity_error)
        integrity_error = False
        try:
            mommy.make(ClaimList, _quantity=3, user=user, deal=deal)
        except IntegrityError:
            integrity_error = True
        self.assertTrue(integrity_error)
        integrity_error = False
        try:
            mommy.make(BuryList, _quantity=3, user=user, deal=deal)
        except IntegrityError:
            integrity_error = True
        self.assertTrue(integrity_error)

    def test_nbr_updates(self):
        list = mommy.make(RateList)
        self.assertTrue(list.nbr_updates, 1)
        list.save()
        self.assertTrue(list.nbr_updates, 2)


class RateListTest(TestCase):
    def test_add_review(self):
        list = mommy.make(RateList)
        self.assertTrue(list.nbr_updates, 1)
        self.assertEqual(list.is_active, True)
        list.add_review(review='test', commit=False)
        self.assertEqual(list.review, 'test')
        self.assertTrue(list.nbr_updates, 1)
        list.save()
        self.assertTrue(list.nbr_updates, 2)
        list.add_review(review='')
        self.assertEqual(list.review, 'test')
        list.remove_review(commit=True)
        self.assertEqual(list.review, '')
        self.assertEqual(list.is_active, False)
        self.assertTrue(list.nbr_updates, 3)

    def test_upvote(self):
        list = mommy.prepare(RateList)
        self.assertEqual(list.rating, RateList.NULL_VOTE)
        a, b = list.nullvote(commit=False)
        self.assertEqual(list.rating, RateList.NULL_VOTE)
        self.assertEqual(a, 0)
        self.assertEqual(b, 0)

    def test_upvote(self):
        list = mommy.prepare(RateList)
        self.assertEqual(list.rating, RateList.NULL_VOTE)
        a, b = list.upvote(commit=False)
        self.assertEqual(list.rating, RateList.UP_VOTE)
        self.assertEqual(a, 1)
        self.assertEqual(b, 0)
        a, b = list.upvote(commit=False)
        self.assertEqual(list.rating, RateList.NULL_VOTE)
        self.assertEqual(a, -1)
        self.assertEqual(b, 0)

    def test_downvote(self):
        list = mommy.prepare(RateList)
        self.assertEqual(list.rating, RateList.NULL_VOTE)
        a, b = list.downvote(commit=False)
        self.assertEqual(list.rating, RateList.DOWN_VOTE)
        self.assertEqual(a, 0)
        self.assertEqual(b, 1)
        a, b = list.downvote(commit=False)
        self.assertEqual(list.rating, RateList.NULL_VOTE)
        self.assertEqual(a, 0)
        self.assertEqual(b, -1)

    def test_vote(self):
        list = mommy.prepare(RateList)
        self.assertEqual(list.rating, RateList.NULL_VOTE)
        a, b = list.downvote(commit=False)
        self.assertEqual(list.rating, RateList.DOWN_VOTE)
        self.assertEqual(a, 0)
        self.assertEqual(b, 1)
        a, b = list.upvote(commit=False)
        self.assertEqual(list.rating, RateList.UP_VOTE)
        self.assertEqual(a, 1)
        self.assertEqual(b, -1)
        a, b = list.downvote(commit=False)
        self.assertEqual(list.rating, RateList.DOWN_VOTE)
        self.assertEqual(a, -1)
        self.assertEqual(b, 1)
        a, b = list.nullvote(commit=False)
        self.assertEqual(list.rating, RateList.NULL_VOTE)
        self.assertEqual(a, 0)
        self.assertEqual(b, -1)
        a, b = list.upvote(commit=False)
        self.assertEqual(list.rating, RateList.UP_VOTE)
        self.assertEqual(a, 1)
        self.assertEqual(b, 0)
        a, b = list.nullvote(commit=False)
        self.assertEqual(list.rating, RateList.NULL_VOTE)
        self.assertEqual(a, -1)
        self.assertEqual(b, 0)


class ShareListTest(TestCase):
    def test_add_platforms(self):
        list = mommy.make(ShareList)
        self.assertEqual(list.platforms, '[]')
        list.add_platforms('facebook', commit=False)
        self.assertEqual(list.platforms, '["facebook"]')
        list.add_platforms('twitter', 'reddit', commit=False)
        self.assertIn('twitter', eval(list.platforms))
        self.assertEqual(len(eval(list.platforms)), 3)
        list.add_platforms('pinterest')
        self.assertEqual(len(eval(list.platforms)), 4)
        self.assertEqual(list.nbr_updates, 2)


class ViewListTest(TestCase):
    def test_redirect(self):
        list = mommy.make(ViewList)
        self.assertFalse(list.is_redirected)
        list.redirect()
        self.assertTrue(list.is_redirected)


class WishListTest(TestCase):
    def test_remove_form_wishlist(self):
        list = mommy.make(WishList)
        self.assertTrue(list.is_active)
        list.remove_from_list()
        self.assertFalse(list.is_active)


class WishWalletTest(TestCase):
    def test_remove_form_walletlist(self):
        list = mommy.make(WalletList)
        self.assertTrue(list.is_active)
        list.remove_from_list()
        self.assertFalse(list.is_active)


class ClaimListTest(TestCase):
    def test_remove_form_claimlist(self):
        list = mommy.make(ClaimList)
        self.assertTrue(list.is_active)
        list.remove_from_list()
        self.assertFalse(list.is_active)


class BuryListTest(TestCase):
    def test_remove_form_burylist(self):
        list = mommy.make(BuryList)
        self.assertTrue(list.is_active)
        list.remove_from_list()
        self.assertFalse(list.is_active)
