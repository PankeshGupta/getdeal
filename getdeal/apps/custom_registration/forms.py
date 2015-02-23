# -*- coding: utf-8 -*-
"""
Created on Nov 02, 2013
"""

from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _


class RegistrationForm(forms.Form):
    """
    Form for registering a new user account.

    Validates that the requested email is not already in use.
    """

    GENDER = (
        ('1', _(u'Homme')),
        ('2', _(u'Femme')),
    )

    required_css_class = 'required'

    username = forms.EmailField(label=_('E-mail'),
                                required=False,
                                widget=forms.HiddenInput())
    email = forms.EmailField(label=_('E-mail'))
    password = forms.CharField(widget=forms.PasswordInput,
                               label=_('Password'),
                               min_length=8,
                               error_messages={'invalid': _(u"Minimum 8 caractères.")})
    gender = forms.ChoiceField(widget=forms.RadioSelect(), label=_('Sexe'), choices=GENDER)
    honeypot = forms.CharField(required=False,
                               label=_('If you enter anything in this field ' \
                                       'your comment will be treated as spam'))

    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(
                _('This email address is already in use. Please supply a different email address.'))
        return self.cleaned_data['email']
