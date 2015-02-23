# -*- coding: utf-8 -*-
"""
Created on Sep 22, 2013
"""
import datetime

from django.contrib.auth.models import User
from django.db import models

from apps.profiles.models import Profile


class ShouldFollowOtherUsers(Exception):
    pass


class ActiveFriendshipManager(models.Manager):

    def get_query_set(self):
        return super(ActiveFriendshipManager, self).get_query_set().filter(status=True)

    def is_follower(self, from_user, to_user):
        """
        checks for followship relation
        """
        if from_user == to_user:
            return True
        if self.filter(from_user=from_user, to_user=to_user).count() > 0:
            return True
        return False

    def get_followers(self, to_user, profile=False, from_user_request=None):
        """
        Returns all followers for a specific user
        """
        followers = []
        if profile:
            for friendship in self.filter(to_user=to_user).select_related('from_user'):
                obj = Profile.objects.get(user=friendship.from_user)
                if from_user_request is not None:
                    #set following property of profile to true if the current friendship.from_user
                    #is followed by from_user_request
                    #i.e: from_user_request is viewing all followers of to_user
                    #     [should be able to tell if he follow each user in the list]
                    obj.set_following(self.is_follower(from_user_request, friendship.from_user))
                followers.append(obj)
        else:
            for friendship in self.filter(to_user=to_user).select_related('from_user'):
                followers.append(friendship.from_user)
        return followers

    def get_followed(self, from_user, profile=False, to_user_request=None):
        """
        Returns all followed for a specific user
        """
        followed = []
        if profile:
            for friendship in self.filter(from_user=from_user).select_related('to_user'):
                obj = Profile.objects.get(user=friendship.to_user)
                if to_user_request is not None:
                    #set following property of profile to true if the current friendship.to_user
                    #is followed by userf
                    obj.set_following(self.is_follower(to_user_request, friendship.to_user))
                followed.append(obj)
        else:
            for friendship in self.filter(from_user=from_user).select_related('to_user'):
                followed.append(friendship.to_user)
        return followed


class Friendship(models.Model):
    """
    A friendship is a bi-directional association between two users who
    have both agreed to the association.
    """
    to_user = models.ForeignKey(User, related_name="friends_to")
    from_user = models.ForeignKey(User, related_name="friends_from")
    created_at = models.DateField(default=datetime.date.today)
    status = models.BooleanField(default=True)

    objects = models.Manager()
    active = ActiveFriendshipManager()

    class Meta:
        unique_together = (('to_user', 'from_user'),)

    def __unicode__(self):
        return "from %s to %s" % (self.from_user, self.to_user)

    def save(self, *args, **kwargs):
        if self.to_user == self.from_user:
            raise ShouldFollowOtherUsers
        super(Friendship, self).save(*args, **kwargs)

    def block(self, commit=True):
        """
        block a relation between two people
        both wouldn't be able to access to each other profile
        """
        if not self.status:
            return
        self.status = False
        if commit:
            self.save()

    def reactivate(self, commit=True):
        """
        reactivate relation
        """
        if self.status:
            return
        self.status = True
        if commit:
            self.save()


def follow(friendship):
    """
    This will increment the stats of each user:
        nbr_followers, nbr_following
    """
    to_user_profile = friendship.to_user.profile
    to_user_profile.current_stats.nbr_followers += 1
    to_user_profile.current_stats.save()
    from_user_profile = friendship.from_user.profile
    from_user_profile.current_stats.nbr_following += 1
    from_user_profile.current_stats.save()


def unfollow(friendship):
    """
    This will decrement the stats of each user:
        nbr_followers, nbr_following
    It will also increment the nbr_unfollowed
    """
    to_user_profile = friendship.to_user.profile
    to_user_profile.current_stats.nbr_followers -= 1
    to_user_profile.current_stats.save()
    from_user_profile = friendship.from_user.profile
    from_user_profile.current_stats.nbr_following -= 1
    from_user_profile.current_stats.nbr_unfollowed += 1
    from_user_profile.current_stats.save()
