# -*- coding: utf-8 -*-
"""
Created on Sep 17, 2013
"""
from celery import task

from scrapers.crawler import ScrapydProcess


@task(ignore_result=True, queue='spiders')
def spider_task(spider_name):
    cp = ScrapydProcess(spider_name)
    cp.start()
