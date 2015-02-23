# -*- coding: utf-8 -*-
"""
Created on Sep 12, 2013
"""
import urllib
import urllib2
import time
import json

from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess

from apps.addresses.models import CityMapping
from apps.categories.models import CategoryMapping
from apps.dsites.models import DSite


class ScrapydProcess(object):

    def __init__(self, dsite_name='', updating=False):
        self.updating = updating
        self.dsite = DSite.objects.get(name=dsite_name)

    def _add_to_crawler(self, city_mapping_pk=None, category_mapping_pk=None):
        param_dict = {
            'project': 'default',
            'spider': self.dsite.name,
            'dsite_pk': self.dsite.pk,
            'city_mapping_pk': city_mapping_pk,
            'category_mapping_pk': category_mapping_pk,
            'updating': self.updating,
        }
        params = urllib.urlencode(param_dict)
        req = urllib2.Request('http://localhost:6800/schedule.json', params)
        response = urllib2.urlopen(req)
        time.sleep(3)

    def start(self):
        if self.dsite.has_both_mappings:
            for city_mapping in CityMapping.objects.filter(dsite=self.dsite):
                for category_mapping in CategoryMapping.objects.filter(dsite=self.dsite, all_cities=False):
                    self._add_to_crawler(category_mapping_pk=category_mapping.pk,
                                         city_mapping_pk=city_mapping.pk)
            if self.dsite.has_category_mapping:
                for category_mapping in CategoryMapping.objects.filter(dsite=self.dsite, all_cities=True):
                    self._add_to_crawler(category_mapping_pk=category_mapping.pk)
        elif self.dsite.has_city_mapping:
            for city_mapping in CityMapping.objects.filter(dsite=self.dsite):
                self._add_to_crawler(city_mapping_pk=city_mapping.pk)
            if self.dsite.has_category_mapping:
                for category_mapping in CategoryMapping.objects.filter(dsite=self.dsite, all_cities=True):
                    self._add_to_crawler(category_mapping_pk=category_mapping.pk)
        elif self.dsite.has_category_mapping:
            for category_mapping in CategoryMapping.objects.filter(dsite=self.dsite):
                self._add_to_crawler(category_mapping_pk=category_mapping.pk)

    @staticmethod
    def stop_job(job_id):
        param_dict = {
            'project': 'default',
            'job': job_id
        }
        params = urllib.urlencode(param_dict)
        req = urllib2.Request('http://localhost:6800/cancel.json', params)
        response = urllib2.urlopen(req)

    def pending_jobs_for(self, spider=''):
        """
        Return number of pending jobs for this spider
        """
        resp = urllib2.urlopen('http://localhost:6800/listjobs.json?project=default')
        data = json.load(resp)
        spider = spider if spider else self.dsite.name
        nbr_jobs = 0
        if 'pending' in data:
            for item in data['pending']:
                if item['spider'] == spider:
                    nbr_jobs += 1
        return nbr_jobs

    def running_jobs_for(self, spider=''):
        """
        Return number of running jobs for this spider
        """
        resp = urllib2.urlopen('http://localhost:6800/listjobs.json?project=default')
        data = json.load(resp)
        spider = spider if spider else self.dsite.name
        nbr_jobs = 0
        if 'pending' in data:
            for item in data['pending']:
                if item['spider'] == spider:
                    nbr_jobs += 1
        return nbr_jobs

    def finished_jobs_for(self, spider=''):
        """
        Return number of finished jobs for this spider
        """
        resp = urllib2.urlopen('http://localhost:6800/listjobs.json?project=default')
        data = json.load(resp)
        spider = spider if spider else self.dsite.name
        nbr_jobs = 0
        if 'finished' in data:
            for item in data['finished']:
                if item['spider'] == spider:
                    nbr_jobs += 1
        return nbr_jobs

    @staticmethod
    def list_spiders():
        """
        Returns list spiders
        """
        resp = urllib2.urlopen('http://localhost:6800/listspiders.json?project=default')
        data = json.load(resp)
        if 'spiders' in data:
            return data['spiders']

    def clear_job_for(self, spider='', all=False):
        resp = urllib2.urlopen('http://localhost:6800/listjobs.json?project=default')
        data = json.load(resp)
        spider = spider if spider else self.dsite.name
        if 'pending' in data:
            for item in data['pending']:
                if not all:
                    if item['spider'] == spider:
                        self.stop_job(item['id'])
                else:
                    self.stop_job(item['id'])


class CrawlerProcessScript(object):
    """
        Creates multiple crawlers and call them sequentially
        Crawler names should follow this naming convention:
            spider_name + _ + city + _ + category
        crawlers : keeps track of all crawlers run, so to get their stats after they are finished.
    """

    def __init__(self, dsite_name='', updating=False):
        self.updating = str(updating)
        self.dsite = DSite.objects.get(name=dsite_name)
        self.crawler_process = CrawlerProcess(get_project_settings())
        self.crawlers = {}

    def _add_crawler(self, crawler_name, city_mapping_pk=None, category_mapping_pk=None):
        crawler = self.crawler_process.create_crawler(crawler_name)
        spider = crawler.spiders.create(self.dsite.name, dsite_pk=self.dsite.pk, city_mapping_pk=city_mapping_pk,
                                        category_mapping_pk=category_mapping_pk, updating=self.updating)
        crawler.crawl(spider)
        self.crawlers[crawler_name] = crawler

    def _create_crawlers(self):
        if self.dsite.has_both_mappings:
            for city_mapping in CityMapping.objects.filter(dsite=self.dsite):
                for category_mapping in CategoryMapping.objects.filter(dsite=self.dsite, all_cities=False):
                    crawler_name = self.dsite.name + '_' + city_mapping.site_city + '_' + category_mapping.site_category
                    self._add_crawler(crawler_name=crawler_name, category_mapping_pk=category_mapping.pk,
                                      city_mapping_pk=city_mapping.pk)
            if self.dsite.has_category_mapping:
                for category_mapping in CategoryMapping.objects.filter(dsite=self.dsite, all_cities=True):
                    crawler_name = self.dsite.name + '_' + category_mapping.site_category
                    self._add_crawler(crawler_name=crawler_name, category_mapping_pk=category_mapping.pk)
        elif self.dsite.has_city_mapping:
            for city_mapping in CityMapping.objects.filter(dsite=self.dsite):
                crawler_name = self.dsite.name + '_' + city_mapping.site_city
                self._add_crawler(crawler_name=crawler_name, city_mapping_pk=city_mapping.pk)
            if self.dsite.has_category_mapping:
                for category_mapping in CategoryMapping.objects.filter(dsite=self.dsite, all_cities=True):
                    crawler_name = self.dsite.name + '_' + category_mapping.site_category
                    self._add_crawler(crawler_name=crawler_name, category_mapping_pk=category_mapping.pk)
        elif self.dsite.has_category_mapping:
            for category_mapping in CategoryMapping.objects.filter(dsite=self.dsite):
                crawler_name = self.dsite.name + '_' + category_mapping.site_category
            self._add_crawler(crawler_name=crawler_name, category_mapping_pk=category_mapping.pk)

    def start(self):
        self._create_crawlers()
        self.crawler_process.start()
        self.crawler_process.stop()
        self.crawler_process.stop_reactor()

    def dump_stats(self):
        for crawler_name, crawler in self.crawlers.iteritems():
            print crawler_name
            print crawler.stats.get_stats()
