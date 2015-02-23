# -*- coding: utf-8 -*-
"""
Created on Dec 27, 2013
"""
from django import forms
from django.contrib.auth.models import User
from django.forms import (
    CharField,
    Form,
    PasswordInput,
    ValidationError,
)
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from .models import Preferences


class ProfileForm(Form):
    """
    The ProfileForm provides a form used to update the user's informations
    """
    GENDER = (
        ('0', u'--'),
        ('1', _(u'Homme')),
        ('2', _(u'Femme')),
    )

    required_css_class = 'required'

    first_name = forms.CharField(label=_(u'Nom'), required=False)
    last_name = forms.CharField(label=_(u'Prénom'), required=False)
    email = forms.EmailField(label=_('E-mail'), required=False)
    gender = forms.ChoiceField(widget=forms.Select(), label=_('Sexe'), choices=GENDER,
                               required=False)

    def __init__(self, profile, *args, **kwargs):
        """
        Initializes a new instance of the ChangePasswordForm class.
        """
        self.profile = profile
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].initial = profile.user.first_name
        self.fields['last_name'].initial = profile.user.last_name
        self.fields['email'].initial = profile.user.email
        self.fields['email'].gender = profile.gender

    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        """
        users = User.objects.filter(email__iexact=self.cleaned_data['email'])
        if users.exists():
            if users[0] != self.profile.user:
                raise forms.ValidationError(
                    _('This email address is already in use. Please supply a different email address.'))
        return self.cleaned_data['email']

    def save(self):
        """
        Applies the new password to the user and saves it.
        """
        profile = self.profile
        gender = self.cleaned_data.get('gender')
        profile.gender = gender
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        profile.user.first_name = first_name
        profile.user.last_name = last_name
        email = self.cleaned_data.get('email')
        profile.user.email = email
        profile.user.save()
        profile.save()
        return profile


class ChangePasswordForm(Form):
    """
    The ChangePasswordForm provides a form used to validate changing password
    information.
    """
    current = CharField(
        label=_('Current password'),
        min_length=8,
        max_length=128,
        widget=PasswordInput())
    new = CharField(
        label=_('New password'),
        min_length=8,
        max_length=128,
        widget=PasswordInput())
    confirm = CharField(
        label=_('Confirm new password'),
        min_length=8,
        max_length=128,
        widget=PasswordInput())

    def __init__(self, user, *args, **kwargs):
        """
        Initializes a new instance of the ChangePasswordForm class.
        """
        self.user = user
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_current(self):
        """
        Validates the current password by checking it with the user.
        """
        password = self.cleaned_data.get('current')
        if not self.user.check_password(password):
            raise ValidationError(_('The current password was incorrect.'))

        return password

    def clean_confirm(self):
        """
        Validates the confirmation password by checking if it matches the new
        password.
        """
        new_password = self.cleaned_data.get('new')
        confirm_password = self.cleaned_data.get('confirm')
        if new_password and confirm_password and new_password != confirm_password:
            raise ValidationError(_('The new and confirm passwords did not match.'))

        return confirm_password

    def clean(self):
        """
        Validates the form by checking if the applied user account.
        """
        if not self.user.is_active:
            raise ValidationError(_('Invalid user account.'))

        return self.cleaned_data

    def save(self):
        """
        Applies the new password to the user and saves it.
        """
        new_password = self.cleaned_data.get('new')
        user = self.user
        user.set_password(new_password)
        user.save()
        return user


class NewsLetterForm(Form):
    """
    The NewsLetterForm provides a form used to update the user's newsletter preferences
    """
    required_css_class = 'required'

    newsletter_frequency = forms.ChoiceField(widget=forms.RadioSelect(), label=_(u'Fréquence des e-mails'),
                                             choices=Preferences.FREQUENCIES,
                                             required=False)
    paused_until = forms.DateField(required=False, label=_(u'Jusqu\'au'))

    def __init__(self, preferences, *args, **kwargs):
        """
        Initializes a new instance of the ChangePasswordForm class.
        """
        self.preferences = preferences
        super(NewsLetterForm, self).__init__(*args, **kwargs)
        self.fields['newsletter_frequency'].initial = preferences.newsletter_frequency
        if preferences.paused_until and preferences.paused_until > now().date():
            self.fields['paused_until'].initial = preferences.paused_until

    def save(self):
        """
        Applies the new password to the user and saves it.
        """
        preferences = self.preferences
        preferences.newsletter_frequency = self.cleaned_data.get('newsletter_frequency')
        paused_until = self.cleaned_data.get('paused_until')
        if paused_until:
            preferences.paused_until = paused_until
        preferences.save()
        return preferences
