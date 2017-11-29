# -*- coding: utf-8 -*-
"""Custom account adapters for django-allauth.

These are used in order to extend the default authorization provided by
django-allauth.

"""
import string
import logging
import traceback

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.module_loading import import_string

from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_field
from allauth.account.utils import user_email
from allauth.account.utils import user_username
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from geonode.people.adapters import LocalAccountAdapter

logger = logging.getLogger(__name__)


def populate_username(first_name, last_name):
    fname = u''.join(e for e in first_name if e in string.ascii_letters or '-' == e).lower()
    lname = u''.join(e for e in last_name if e in string.ascii_letters or '-' == e).lower()
    printable = set(string.printable)
    return filter(lambda x: x in printable, u'{}.{}'.format(fname, lname).encode('utf-8').strip())


class UnescoLocalAccountAdapter(LocalAccountAdapter):
    """Customizations for local accounts

    Check `django-allauth's documentation`_ for more details on this class.

    .. _django-allauth's documentation:
       http://django-allauth.readthedocs.io/en/latest/advanced.html#creating-and-populating-user-instances

    """

    def populate_username(self, request, user):
        # validate the already generated username with django validation
        # if it passes use that, otherwise use django-allauth's way of
        # generating a unique username
        try:
            # safe_username = user_username(user)
            safe_username = populate_username(user_field(user, 'first_name'), user_field(user, 'last_name'))
            user.username = safe_username
            user.full_clean()
        except ValidationError:
            traceback.print_exc()
            safe_username = self.generate_unique_username([
                user_field(user, 'first_name'),
                user_field(user, 'last_name'),
                user_email(user),
                user_username(user)
            ])
        user_username(user, safe_username)