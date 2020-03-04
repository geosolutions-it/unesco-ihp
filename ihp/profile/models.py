# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2016 OSGeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

from uuid import uuid4
import logging

from django.conf import settings

from django.db import models
from django.core.mail import send_mail
from django.db.models import signals

from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.signals import user_logged_in, user_logged_out

from taggit.managers import TaggableManager

from geonode.base.enumerations import COUNTRIES
from geonode.groups.models import GroupProfile
# from geonode.notifications_helper import send_notification

from allauth.account.signals import user_signed_up
from allauth.socialaccount.signals import social_account_added
# from account.models import EmailAddress

from geonode.people.models import Profile, ProfileUserManager
from geonode.people.utils import format_address
from geonode.people.signals import (
    do_login,
    do_logout,
    update_user_email_addresses,
    notify_admins_new_signup)
from geonode.people.languages import LANGUAGES
from geonode.people.timezones import TIMEZONES

logger = logging.getLogger(__name__)

email_subject = """Welcome to IHP-WINS/Bienvenue sur IHP-WINS"""

email_format = """Dear contributor,

Your account ({}) has been approved and is now active on the Water Information Network System.
You can now log in to {}

To manage your account, please go to {}/notifications/settings/

The IHP-WINS Team

----------------------------------------------------

Cher contributeur,

Votre compte ({}) a ete approuve et est desormais actif sur le Systeme de Reseau d'Informations sur l'Eau.
Vous pouvez des a present vous connecter sur {}

Pour gerer votre compte, rendez-vous sur {}/notifications/settings/

L'equipe IHP-WINS"""


class IHPProfile(Profile):

    """Fully featured Geonode user"""

    approved = models.BooleanField(
        _('Is the user approved?'),
        default=False,
        help_text=_('approve user'))
    recommendation = models.CharField(
        max_length=50,
        default="",
        blank=True,
        null=True,
        help_text=_('Name of the person who recommended you IHP-WINS'))


def profile_post_save(instance, sender, **kwargs):
    """
    Make sure the user belongs by default to the anonymous group.
    This will make sure that anonymous permissions will be granted to the new users.
    """
    from django.contrib.auth.models import Group
    anon_group, created = Group.objects.get_or_create(name='anonymous')
    instance.groups.add(anon_group)
    # do not create email, when user-account signup code is in use
    if getattr(instance, '_disable_account_creation', False):
        return


def profile_pre_save(instance, sender, **kw):
    matching_profiles = IHPProfile.objects.filter(id=instance.id)
    if matching_profiles.count() == 0:
        return
    if instance.is_active and not matching_profiles.get().is_active:
        # send_notification((instance,), "account_active")
        if not instance.approved:
            instance.approved = True
            message = email_format.format(instance.username, settings.SITEURL, settings.SITEURL,
                                          instance.username, settings.SITEURL, settings.SITEURL)
            try:
                send_mail(
                    email_subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [instance.email],
                    fail_silently=True,
                )
            except BaseException:
                import traceback
                traceback.print_exc()


""" Connect relevant signals to their corresponding handlers. """
user_logged_in.connect(do_login)
user_logged_out.connect(do_logout)
social_account_added.connect(
    update_user_email_addresses,
    dispatch_uid=str(uuid4()),
    weak=False
)
user_signed_up.connect(
    notify_admins_new_signup,
    dispatch_uid=str(uuid4()),
    weak=False
)
signals.pre_save.connect(
    profile_pre_save,
    sender=IHPProfile
)
signals.post_save.connect(
    profile_post_save,
    sender=IHPProfile
)

