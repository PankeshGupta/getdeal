# -*- coding: utf-8 -*-
"""
Created on Sep 17, 2013
"""
from scrapy.exceptions import IgnoreRequest

from apps.deals.models import Deal


class IgnoreDownloaderMiddleware(object):
    def process_request(self, request, spider):
        if not spider.updating:
            if spider.city_mapping is not None:
                deal_exists = Deal.objects.filter(url=request.url, city=spider.city_mapping.target_city).exists()
            else:
                deal_exists = Deal.objects.filter(url=request.url).exists()
            if deal_exists:
                raise IgnoreRequest("This item (%s) already exists, and we are not updating." % request.url)
        return None
