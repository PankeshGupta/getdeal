# -*- coding: utf-8 -*-
"""
Created on Aug 23, 2013
"""
from __future__ import absolute_import

from geopy import geocoders
from geopy.geocoders.base import GeocoderResultError

from django.utils.encoding import smart_str


class GeoError(Exception):
    pass


def google_v3(address):
    """
    Given an address, return ``(computed_address, (latitude, longitude))``
    tuple using Google Geocoding API v3.
    """
    try:
        g = geocoders.GoogleV3()
        address = smart_str(address)
        return g.geocode(address, exactly_one=False)[0]
    except (UnboundLocalError, ValueError, GeocoderResultError) as e:
        raise GeoError(e)
