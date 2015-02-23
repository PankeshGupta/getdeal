# -*- coding: utf-8 -*-
"""
Created on Dec 27, 2013
"""

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.shortcuts import HttpResponseRedirect
from apps.lists.models import RateList

from apps.subscriptions.models import CitySubscription
from .models import Profile
from .forms import ProfileForm, ChangePasswordForm, NewsLetterForm


class ProfileView(TemplateView):
    """
    The ProfileView class provides a template-based view used to view the user profile
    """
    template_name = 'profiles/view.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """
        GET request handler.
        """
        rates = RateList.objects.filter(user=request.user)
        rates_counts = rates.values('deal__category__slug',
                                    'deal__category__name').annotate(count_by_category=
                                                            Count('deal__category__slug'))
        context = {'profile': Profile.objects.get(user=request.user),
                   'rates_counts': rates_counts}
        return render(request, self.template_name, context)


class ProfileRatesView(TemplateView):
    """
    The ProfileRatesView class provides a template-based view used to view the rates
    by a user
    """
    template_name = 'profiles/rates.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """
        GET request handler.
        """
        context = {'profile': Profile.objects.get(user=request.user)}
        return render(request, self.template_name, context)


class EditProfileView(TemplateView):
    """
    The EditProfileView class provides a template-based view used to edit the user profile
    """
    template_name = 'profiles/edit.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """
        GET request handler.
        """
        context = {'form': ProfileForm(Profile.objects.get(user=request.user))}
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """
        POST request handler.
        """
        form = ProfileForm(Profile.objects.get(user=request.user), request.POST)
        if form.is_valid():
            form.save()
        return render(request, self.template_name, {'form': form})


class ChangePasswordView(TemplateView):
    """
    The ChangePasswordView class provides a template-based view used to change
    the password of a currently logged in user.
    """
    template_name = 'profiles/change_password.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """
        GET request handler.
        """
        context = {'form': ChangePasswordForm(request.user)}
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """
        POST request handler.
        """
        user = request.user
        form = ChangePasswordForm(user, request.POST)
        if form.is_valid():
            # apply new password
            form.save()
        return render(request, self.template_name, {'form': form})


class CitiesManagementView(TemplateView):
    """
    Manage cities' subscriptions
    """

    template_name = 'profiles/cities_subscriptions.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """
        GET request handler.
        """
        cities_subscriptions = request.user.cities_subscriptions.filter(is_active=True)
        context = {'cities_subscriptions': cities_subscriptions}
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """
        POST request handler.
        """
        subscription_pk = request.POST.get('subscription_pk', '')
        next = request.POST.get('next', '')
        if subscription_pk:
            try:
                CitySubscription.objects.get(pk=subscription_pk).deactivate()
            except CitySubscription.DoesNotExist:
                pass
        if next:
            return HttpResponseRedirect(next)
        return HttpResponseRedirect(reverse('profiles:city-preferences'))


class NewsletterPreferencesView(TemplateView):
    """
    The EditNewsletterPreferencesView class provides a template-based view used
    to edit the user newsletter preferences
    """
    template_name = 'profiles/edit_newsletter.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """
        GET request handler.
        """
        context = {'form': NewsLetterForm(Profile.objects.get(user=request.user).preferences)}
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """
        POST request handler.
        """
        form = NewsLetterForm(Profile.objects.get(user=request.user).preferences, request.POST)
        if form.is_valid():
            form.save()
        return render(request, self.template_name, {'form': form})
