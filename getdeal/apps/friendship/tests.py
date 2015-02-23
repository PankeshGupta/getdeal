# -*- coding: utf-8 -*-
"""
Created on Sep 22, 2013
"""
from model_mommy import mommy

from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.test import TestCase

from apps.friendship.models import Friendship, ShouldFollowOtherUsers


class FriendshipTest(TestCase):
    def test_mapping_creation(self):
        friendship = mommy.make(Friendship)
        self.assertTrue(isinstance(friendship, Friendship))
        self.assertEqual(friendship.__unicode__(), 'from %s to %s' %
                                                   (friendship.from_user, friendship.to_user))

    def test_integrity(self):
        users = mommy.make(User, _quantity=2)
        error_occurred = False
        try:
            mommy.make(Friendship, _quantity=2, from_user=users[0], to_user=users[1])
        except IntegrityError:
            error_occurred = True
        self.assertTrue(error_occurred)

    def test_follow_oneself(self):
        user = mommy.make(User)
        error_occurred = False
        try:
            mommy.make(Friendship, from_user=user, to_user=user)
        except ShouldFollowOtherUsers:
            error_occurred = True
        self.assertTrue(error_occurred)

    def test_block(self):
        friendship = mommy.make(Friendship)
        friendship.block()
        self.assertEqual(friendship.status, False)
        friendship.reactivate()
        self.assertEqual(friendship.status, True)

    def test_creation_date(self):
        friendship = mommy.make(Friendship)
        date1 = friendship.created_at
        friendship.active = False
        friendship.save()
        date2 = friendship.created_at
        self.assertEqual(date1, date2)

    def test_is_follower(self):
        to_user = mommy.make(User)
        from_user = mommy.make(User)
        mommy.make(Friendship, to_user=to_user, from_user=from_user)
        self.assertTrue(Friendship.active.is_follower(from_user=from_user, to_user=to_user))
        self.assertFalse(Friendship.active.is_follower(from_user=to_user, to_user=from_user))

    def test_followers(self):
        user = mommy.make(User)
        friendships = mommy.make(Friendship, _quantity=3, to_user=user)
        self.assertEqual(len(Friendship.active.get_followers(to_user=user)), 3)
        friendships[0].block()
        friendships[0].save()
        self.assertEqual(len(Friendship.active.get_followers(to_user=user)), 2)

    def test_followed(self):
        user = mommy.make(User)
        friendships = mommy.make(Friendship, _quantity=3, from_user=user)
        self.assertEqual(len(Friendship.active.get_followed(from_user=user)), 3)
        friendships[0].block()
        friendships[0].save()
        self.assertEqual(len(Friendship.active.get_followed(from_user=user)), 2)
