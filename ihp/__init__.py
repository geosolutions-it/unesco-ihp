# -*- coding: utf-8 -*-
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

import re
import string
import logging
from django.apps import AppConfig
from django.db import models
from django.utils.translation import ugettext_lazy as _

alnum_re = re.compile(r'^[a-zA-Z][A-Za-z_-]*$')


def populate_username(first_name, last_name):
    fname = u''.join(e for e in first_name if e in string.ascii_letters or '-' == e).lower()
    lname = u''.join(e for e in last_name if e in string.ascii_letters or '-' == e).lower()
    printable = set(string.printable)
    return filter(lambda x: x in printable, u'{}.{}'.format(fname, lname).encode('utf-8').strip())


class IHPAppConfig(AppConfig):
    name = 'ihp'

    def _get_logger(self):
        return logging.getLogger(self.__class__.__module__)

    def patch_resource_base(self, cls):
        self._get_logger().info("Patching Resource Base")
        doi_help_text = _(
            'a DOI will be added by Admin before publication.')
        doi = models.TextField(
            _('DOI'),
            blank=True,
            null=True,
            help_text=doi_help_text)
        cls.add_to_class('doi', doi)
        # cls._meta.add_field(doi)

    def run_setup_hooks(self, *args, **kwargs):
        from django.conf import settings
        from .celeryapp import app as celeryapp
        if 'celeryapp' not in settings.INSTALLED_APPS:
            settings.INSTALLED_APPS += (celeryapp, )

    def ready(self):
        from geonode.base.models import ResourceBase
        self.patch_resource_base(ResourceBase)
        self.run_setup_hooks()


default_app_config = 'ihp.IHPAppConfig'
