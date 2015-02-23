# -*- coding: utf-8 -*-
"""
Created on Sep 22, 2013
"""
from django.db.models import Q


def get_list_related_users(user, direction='to', relation_status="1", random=False, amount=30, q=''):
    list_users = []
    if direction == 'to':
        #followers        
        list = user.friends_to.filter(status=relation_status)
        if not q == '':
            list = list.filter(Q(from_user__first_name__icontains=q) | Q(from_user__last_name__icontains=q) | Q(
                from_user__username_icontains=q))
        if random:
            list = list.order_by('?')[:amount]
        for u in list:
            list_users.append(u.from_user)
        return list_users

    if direction == 'from':
        list = user.friends_from.filter(status=relation_status)
        if not q == '':
            list = list.filter(Q(to_user__first_name__icontains=q) | Q(to_user__last_name__icontains=q) | Q(
                to_user__username__icontains=q))
        if random:
            list = list.order_by('?')[:amount]
        for u in list:
            list_users.append(u.to_user)
        return list_users
