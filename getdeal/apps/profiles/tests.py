# -*- coding: utf-8 -*-
"""
Created on Sep 22, 2013
"""
from model_mommy import mommy

from django.contrib.auth.models import User
from django.db.utils import DatabaseError
from django.test import TestCase

from rest_framework.authtoken.models import Token

from .models import Profile, Preferences, Steps, ProfileStats


class ProfileTest(TestCase):
    def test_profile_creation(self):
        user = mommy.make(User)
        try:
            profile = Profile.objects.get(user=user)
        except DatabaseError:
            profile = None
        self.assertTrue(isinstance(profile, Profile))
        self.assertEqual(profile.__unicode__(), '%s <%s>' % (profile.user, profile.user.email))
        self.assertTrue(isinstance(profile.token, Token))
        self.assertTrue(isinstance(profile.preferences, Preferences))
        self.assertTrue(isinstance(profile.steps, Steps))
        self.assertEqual(profile.current_stats, None)
        self.assertTrue(profile.user.is_active)
        profile.delete_user(confirm=True)
        profile.activate()
        self.assertTrue(profile.user.is_active)
        profile.delete_user(confirm=True)
        self.assertFalse(profile.user.is_active)
        self.assertTrue(user.profile, profile)


class ProfileStatsTest(TestCase):
    def make_profile(self):
        return Profile.objects.get(user=mommy.make(User))

    def test_profile_stats_creation(self):
        profile = self.make_profile()
        profile_stats = mommy.make(ProfileStats, profile=profile)
        self.assertTrue(isinstance(profile_stats, ProfileStats))
        self.assertEqual(profile_stats.counter, 1)
        self.assertEqual(profile_stats.previous, None)
        self.assertEqual(profile_stats.__unicode__(), "profile: %s, counter: %d" % (profile_stats.profile.user,
                                                                                    profile_stats.counter))

    def create_two_instance(self):
        profile = self.make_profile()
        profile_stats = mommy.make(ProfileStats, profile=profile)
        profile_stats.nbr_views = 1
        profile_stats2 = mommy.make(ProfileStats, profile=profile)
        profile_stats2.nbr_views += 1
        return profile, profile_stats, profile_stats2

    def test_counter_increment(self):
        profile, profile_stats, profile_stats2 = self.create_two_instance()
        self.assertEqual(profile_stats.counter, 1)
        self.assertEqual(profile_stats2.counter, 2)
        self.assertEqual(profile_stats.nbr_views, 1)
        self.assertEqual(profile_stats2.nbr_views, 2)

    def test_previous(self):
        profile, profile_stats, profile_stats2 = self.create_two_instance()
        self.assertEqual(profile_stats.previous, None)
        self.assertEqual(profile_stats2.previous, profile_stats)
        self.assertEqual(profile.current_stats, profile_stats2)
