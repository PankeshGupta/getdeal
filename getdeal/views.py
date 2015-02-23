# -*- coding: utf-8 -*-
"""
Created on Aug 19, 2013
"""
from django.shortcuts import render_to_response
from django.template import RequestContext


def home(request, city=None, template_name="index.html"):
    """
    A view that shows all of the wall items.
    (Use template_name of 'wall/recent.html' to see just recent items.)
    """

    if request.user.is_authenticated():
        template_name = "home.html"
    if not city:
        city = 'casablanca'
    return render_to_response(template_name,
                              context_instance=RequestContext(request, {'city': city}))


def about(request, template_name="about.html"):
    """"""
    return render_to_response(template_name, context_instance=RequestContext(request))


def policy(request, template_name="policy.html"):
    """"""
    return render_to_response(template_name, context_instance=RequestContext(request))


def terms(request, template_name="terms.html"):
    """"""
    return render_to_response(template_name, context_instance=RequestContext(request))


def help(request, template_name="help.html"):
    """"""


def careers(request, template_name="careers.html"):
    """"""
    return render_to_response(template_name, context_instance=RequestContext(request))
