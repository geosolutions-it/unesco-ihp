#########################################################################
#
# Copyright (C) 2017 OSGeo
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

"""Pinax Notifications Hooks Override

"""

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist

from pinax.notifications.conf import settings
from pinax.notifications.utils import load_media_defaults


class IHPNotificationsHookSet(object):

    def notice_setting_for_user(self, user, notice_type, medium, scoping=None):
        kwargs = {
            "notice_type": notice_type,
            "medium": medium
        }
        if scoping:
            kwargs.update({
                "scoping_content_type": ContentType.objects.get_for_model(scoping),
                "scoping_object_id": scoping.pk
            })
        else:
            kwargs.update({
                "scoping_content_type__isnull": True,
                "scoping_object_id__isnull": True
            })
        try:
            return user.noticesetting_set.get(**kwargs)
        except ObjectDoesNotExist:
            _, NOTICE_MEDIA_DEFAULTS = load_media_defaults()
            if scoping is None:
                kwargs.pop("scoping_content_type__isnull")
                kwargs.pop("scoping_object_id__isnull")
                kwargs.update({
                    "scoping_content_type": None,
                    "scoping_object_id": None
                })
            # default = (NOTICE_MEDIA_DEFAULTS[medium] <= notice_type.default)

            default = settings.NOTIFICATIONS_ENABLED_BY_DEFAULT
            kwargs.update({"send": default})
            setting = user.noticesetting_set.create(**kwargs)
            return setting
