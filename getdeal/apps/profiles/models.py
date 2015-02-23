# -*- coding: utf-8 -*-
"""
Created on Sep 22, 2013
"""
import time
import hashlib
import redis

from django.utils.timezone import now
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from rest_framework.authtoken.models import Token

from apps.subscriptions.models import (CategorySubscription, SubCategorySubscription,
                                       CitySubscription, SupplierSubscription, DSiteSubscription)

#import logging
#logr = logging.getLogger(__name__)


class Preferences(models.Model):
    """
    User preferences
    """
    FREQUENCIES = (
        ('0', _('Daily')),
        ('1', _('Twice a week')),
        ('2', _('Once a week')),
        ('3', _('Once a month')),
        ('4', _('Never')),
    )

    send_emails = models.BooleanField(default=True)
    view_settings = models.TextField(default='{}')
    newsletter_frequency = models.CharField(max_length=1, default='0', choices=FREQUENCIES)
    paused_until = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = _('Preference')
        verbose_name_plural = _('Preferences')
        app_label = 'profiles'

    def __unicode__(self):
        return "Preferences for %s" % self.profile.user


class Steps(models.Model):
    """
    Tutorial and Steps to check
    """
    tutorial_finished = models.BooleanField(default=False)
    hide_getting_started = models.NullBooleanField(default=False, null=True, blank=True)
    has_setup_feeds = models.NullBooleanField(default=False, null=True, blank=True)
    has_found_friends = models.NullBooleanField(default=False, null=True, blank=True)

    class Meta:
        verbose_name = _('Step')
        verbose_name_plural = _('Steps')
        app_label = 'profiles'

    def __unicode__(self):
        return "Steps for %s" % self.profile.user


class ProfileStats(models.Model):
    """
    Stats for users
    """
    profile = models.ForeignKey('Profile', related_name="stats")
    nbr_following = models.IntegerField(default=0)
    nbr_followers = models.IntegerField(default=0)
    nbr_unfollowed = models.IntegerField(default=0)
    nbr_shared_deals = models.IntegerField(default=0)
    nbr_rated_deals = models.IntegerField(default=0)
    nbr_positive_deals = models.IntegerField(default=0)
    nbr_negative_deals = models.IntegerField(default=0)
    nbr_viewed_deals = models.IntegerField(default=0)
    nbr_wished_deals = models.IntegerField(default=0)
    nbr_bought_deals = models.IntegerField(default=0)
    nbr_claimed_deals = models.IntegerField(default=0)
    nbr_buried_deals = models.IntegerField(default=0)
    nbr_visits = models.IntegerField(default=0)
    nbr_subscriptions = models.IntegerField(default=0)
    nbr_ips = models.IntegerField(default=0)
    last_visit_on = models.DateTimeField(default=now)
    last_visit_ip = models.CharField(max_length=50, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    counter = models.IntegerField(default=1, editable=False)
    previous = models.ForeignKey('self', blank=True, null=True, editable=False)

    class Meta:
        verbose_name = _('Profile statistics')
        verbose_name_plural = _('Profile statistics')
        app_label = 'profiles'

    def __unicode__(self):
        return "profile: %s, counter: %d" % (self.profile.user, self.counter)

    def save(self, **kwargs):
        current_stats = self.profile.current_stats
        if current_stats is not None and self.id is None:
            self.counter = current_stats.counter + 1
            self.nbr_views = current_stats.nbr_views
            self.previous = self.profile.current_stats
        super(ProfileStats, self).save(**kwargs)

    def visit_with_ip(self, ip):
        if self.last_visit_ip != ip:
            self.nbr_ips += 1
        self.nbr_visits += 1
        self.last_visit_ip = ip
        self.last_visit_on = now()
        self.save()


@receiver(post_save, sender=ProfileStats)
def set_profile_stats(sender, *args, **kwargs):
    """
    Signal handler to ensure that a new stats is always chosen as the current stats - automatically. It simplifies stuff
    greatly. Also stores previous revision for diff-purposes
    """
    instance = kwargs['instance']
    created = kwargs['created']
    if created and instance.profile:
        instance.profile.current_stats = instance
        instance.profile.save()


class Profile(models.Model):
    DEFAULT_AVATAR = 'profile.png'

    GENDER = (
        ('0', _('Rather not say')),
        ('1', _('Male')),
        ('2', _('Female')),
    )

    user = models.OneToOneField(User, unique=True, primary_key=True, related_name='profile', editable=False)
    gender = models.CharField(max_length=1, choices=GENDER, default='0', verbose_name=_('Gender'))
    location = models.ManyToManyField('addresses.City', blank=True, null=True)
    #@todo: create timezone field
    timezone = models.CharField(max_length=5, default='UCT')
    token = models.ForeignKey(Token, blank=True, null=True)
    image = models.ImageField(upload_to=settings.AVATAR_STORE + '/full', default=DEFAULT_AVATAR, blank=True, null=True)
    thumbnail = models.ImageField(upload_to=settings.AVATAR_STORE + '/thumb', blank=True, null=True, editable=False)
    preferences = models.OneToOneField('Preferences', unique=True, related_name='profile', editable=False)
    steps = models.OneToOneField('Steps', unique=True, related_name='profile', editable=False)
    current_stats = models.OneToOneField('ProfileStats', blank=True, null=True, editable=False,
                                         related_name='+')

    def __unicode__(self):
        return '%s <%s>' % (self.user, self.user.email)

    @property
    def fullname(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = Token.objects.create(user=self.user)
        if not hasattr(self, 'preferences'):
            self.preferences = Preferences.objects.create()
        if not hasattr(self, 'steps'):
            self.steps = Steps.objects.create()
        super(Profile, self).save(*args, **kwargs)

    def delete_user(self, confirm=False):
        if not confirm:
            print " ---> You must pass confirm=True to delete this user."
            return
        self.user.is_active = False
        self.user.save()

    def activate(self):
        if self.user.is_active:
            return
        self.user.is_active = True
        self.user.save()
        self.send_new_user_email()

    @property
    def get_following(self):
        try:
            return self._following
        except:
            return False

    def set_following(self, follow):
        """
        A property that indicates if the authenticated user is following the current object or user
        """
        self._following = follow

    def _categories_feed(self):
        new_feeds = CategorySubscription.objects.filter(user=self.user,
                                                        category__current_stats__nbr_new_deals__gt=0,
                                                        is_active=True).values('feed_id')
        new_feeds = list(set([f['feed_id'] for f in new_feeds]))
        #@todo: log the feed and its length for this user
        return new_feeds

    def _subcategories_feed(self):
        new_feeds = SubCategorySubscription.objects.filter(user=self.user,
                                                           subcategory__current_stats__nbr_new_deals__gt=0,
                                                           is_active=True).values('feed_id')
        new_feeds = list(set([f['feed_id'] for f in new_feeds]))
        #@todo: log the feed and its length for this user
        return new_feeds

    def _suppliers_feed(self):
        new_feeds = SupplierSubscription.objects.filter(user=self.user,
                                                        supplier__current_stats__nbr_new_deals__gt=0,
                                                        is_active=True).values('feed_id')
        new_feeds = list(set([f['feed_id'] for f in new_feeds]))
        #@todo: log the feed and its length for this user
        return new_feeds

    def _cities_feed(self):
        new_feeds = CitySubscription.objects.filter(user=self.user,
                                                    city__current_stats__nbr_new_deals__gt=0,
                                                    is_active=True).values('feed_id')
        new_feeds = list(set([f['feed_id'] for f in new_feeds]))
        #@todo: log the feed and its length for this user
        return new_feeds

    def _dsite_feed(self):
        new_feeds = DSiteSubscription.objects.filter(user=self.user,
                                                     dsite__current_stats__nbr_new_deals__gt=0,
                                                     is_active=True).values('feed_id')
        new_feeds = list(set([f['feed_id'] for f in new_feeds]))
        #@todo: log the feed and its length for this user
        return new_feeds

    def queue_new_feeds(self, new_feeds=[], type='categoy'):
        if not new_feeds:
            if type == 'category':
                new_feeds.appen(self._categories_feed())
            elif type == 'subcategory':
                new_feeds.appen(self._subcategories_feed())
            elif type == 'city':
                new_feeds.appen(self._cities_feed())
            elif type == 'supplier':
                new_feeds.appen(self._suppliers_feed())
            elif type == 'dsite':
                new_feeds.appen(self._dsite_feed())
            else:  #all
                new_feeds.appen(self._categories_feed())
                new_feeds.appen(self._cities_feed())
                new_feeds.appen(self._suppliers_feed())
                new_feeds.appen(self._dsite_feed())
        size = 4
        for t in (new_feeds[pos:pos + size] for pos in xrange(0, len(new_feeds), size)):
            feed_tasks.new_feeds.apply_async(args=(t,), queue='new_feeds')

    def send_new_user_email(self):
        if not self.user.email or not self.send_emails:
            return

        user = self.user
        text = render_to_string('mail/email_new_account.txt', locals())
        html = render_to_string('mail/email_new_account.xhtml', locals())
        subject = "Welcome to getdeal, %s" % self.user.username
        msg = EmailMultiAlternatives(subject, text,
                                     from_email='getdeal <%s>' % settings.HELLO_EMAIL,
                                     to=['%s <%s>' % (user, user.email)])
        msg.attach_alternative(html, "text/html")
        msg.send(fail_silently=True)
        #@todo : log sending email for new user

    def send_forgot_password_email(self, email=None):
        if not self.user.email and not email:
            print "Please provide an email address."
            return

        if not self.user.email and email:
            self.user.email = email
            self.user.save()

        user = self.user
        text = render_to_string('mail/email_forgot_password.txt', locals())
        html = render_to_string('mail/email_forgot_password.xhtml', locals())
        subject = "Forgot your password on getdeal?"
        msg = EmailMultiAlternatives(subject, text,
                                     from_email='getdeal <%s>' % settings.HELLO_EMAIL,
                                     to=['%s <%s>' % (user, user.email)])
        msg.attach_alternative(html, "text/html")
        msg.send(fail_silently=True)

        #@todo; log sending email for forgotten password: %s" % self.user.email)


@receiver(post_save, sender=User)
def create_profile(sender, instance=None, created=False, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        Profile.objects.get_or_create(user=instance)


def change_password(user, old_password, new_password, only_check=False):
    user_db = authenticate(username=user.username, password=old_password)
    if user_db is None:
        blank = blank_authenticate(user.username)
        if blank and not only_check:
            user.set_password(new_password or user.username)
            user.save()
    if user_db is None:
        user_db = authenticate(username=user.username, password=user.username)

    if not user_db:
        return -1
    else:
        if not only_check:
            user_db.set_password(new_password)
            user_db.save()
        return 1


def blank_authenticate(username, password=""):
    try:
        user = User.objects.get(username__iexact=username)
    except User.DoesNotExist:
        return

    if user.password == "!":
        return user

    algorithm, salt, hash = user.password.split('$', 2)
    encoded_blank = hashlib.sha1(salt + password).hexdigest()
    encoded_username = authenticate(username=username, password=username)
    if encoded_blank == hash or encoded_username == user:
        return user


class RNewUserQueue:
    KEY = "new_user_queue"

    @classmethod
    def activate_next(cls):
        count = cls.user_count()
        if not count:
            return

        user_id = cls.pop_user()
        user = User.objects.get(pk=user_id)
        #@todo : logging.user(user, "~FBActivating free account. %s still in queue." % (count - 1))
        user.profile.activate()

    @classmethod
    def add_user(cls, user_id):
        r = redis.Redis(connection_pool=settings.REDIS_FEED_POOL)
        now = time.time()

        r.zadd(cls.KEY, user_id, now)

    @classmethod
    def user_count(cls):
        r = redis.Redis(connection_pool=settings.REDIS_FEED_POOL)
        count = r.zcard(cls.KEY)

        return count

    @classmethod
    def user_position(cls, user_id):
        r = redis.Redis(connection_pool=settings.REDIS_FEED_POOL)
        position = r.zrank(cls.KEY, user_id)
        if position >= 0:
            return position + 1

    @classmethod
    def pop_user(cls):
        r = redis.Redis(connection_pool=settings.REDIS_FEED_POOL)
        user = r.zrange(cls.KEY, 0, 0)[0]
        r.zrem(cls.KEY, user)

        return user
