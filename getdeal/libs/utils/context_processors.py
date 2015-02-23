# -*- coding: utf-8 -*-
from django.conf import settings

'''
Created on Mar 01, 2011
'''


def SITE(request):
    return {
        'SITE_NAME': settings.SITE_NAME,
        'DEV_ENV': settings.DEV_ENV,
        'PROD_ENV': settings.PROD_ENV,
        'request': request
    }
