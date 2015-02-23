# -*- coding: utf-8 -*-
"""
Created on Aug 25, 2013
"""
import os

from django.conf import settings

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "getdeal.settings")

BOT_NAME = 'scrapers'

SPIDER_MODULES = ['getdeal.scrapers.spiders']

DOWNLOADER_MIDDLEWARES = {
    'getdeal.scrapers.middlewares.IgnoreDownloaderMiddleware': 50,
}

ITEM_PIPELINES = [
    'getdeal.scrapers.pipelines.CheckPipeline',
    'getdeal.scrapers.pipelines.CleanPipeline',
    'scrapy.contrib.pipeline.images.ImagesPipeline',
    'getdeal.scrapers.pipelines.SerializePipeline',
    'getdeal.scrapers.pipelines.StatsCollectionPipeline',
]

DOWNLOAD_DELAY = 0.25

path_to_phatomjs = '../../phantomjs-1.9.1-linux-x86_64/bin/phantomjs'

IMAGES_STORE = settings.MEDIA_ROOT + '/' + settings.IMAGES_STORE
IMAGES_THUMBS = {
    'small': (70, 70),
    'big': (270, 270),
}
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'scrapers (+http://www.yourdomain.com)'
