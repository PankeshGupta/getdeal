# -*- coding: utf-8 -*-
"""
Created on Aug 19, 2013
"""
from model_mommy import mommy

from django.test import TestCase

from models import Deal, DealStats


class DealTest(TestCase):
    def test_deal_creation(self):
        deal = mommy.make(Deal)
        self.assertTrue(isinstance(deal, Deal))
        self.assertEqual(deal.__unicode__(), deal.title)
        self.assertEqual(deal.current_stats, None)


class DealStatsTest(TestCase):
    def test_deal_stats_creation(self):
        deal_stats = mommy.make(DealStats)
        self.assertTrue(isinstance(deal_stats, DealStats))
        self.assertEqual(deal_stats.counter, 1)
        self.assertEqual(deal_stats.score, 0.0)
        self.assertEqual(deal_stats.previous, None)
        self.assertEqual(deal_stats.__unicode__(), "deal: %d, nbr: %d" % (deal_stats.deal.pk,
                                                                          deal_stats.counter))

    def create_two_instance(self):
        deal = mommy.make(Deal)
        deal_stats = mommy.make(DealStats, deal=deal)
        deal_stats.nbr_views = 1
        deal_stats2 = mommy.make(DealStats, deal=deal)
        deal_stats2.nbr_views += 1
        return deal, deal_stats, deal_stats2

    def test_counter_increment(self):
        deal, deal_stats, deal_stats2 = self.create_two_instance()
        self.assertEqual(deal_stats.counter, 1)
        self.assertEqual(deal_stats2.counter, 2)
        self.assertEqual(deal_stats.nbr_views, 1)
        self.assertEqual(deal_stats2.nbr_views, 2)

    def test_previous(self):
        deal, deal_stats, deal_stats2 = self.create_two_instance()
        self.assertEqual(deal_stats.previous, None)
        self.assertEqual(deal_stats2.previous, deal_stats)
        self.assertEqual(deal.current_stats, deal_stats2)
