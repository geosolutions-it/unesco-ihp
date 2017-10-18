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
from django import forms
from django.apps import AppConfig
from django.utils.datastructures import OrderedDict
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _


alnum_re = re.compile(r'^[a-zA-Z][A-Za-z_-]*$')

def populate_username(first_name, last_name):
    fname = u''.join(e for e in first_name if e in string.ascii_letters or '-' == e).lower()
    lname = u''.join(e for e in last_name if e in string.ascii_letters or '-' == e).lower()
    printable = set(string.printable)
    return filter(lambda x: x in printable, u'{}.{}'.format(fname, lname).encode('utf-8').strip())


class IHPAppConfig(AppConfig):
    name = 'ihp'

    def patch_form(self, form_cls):
        form_cls.declared_fields.pop('username', None)

        extra_fields = [
                        ('first_name',
                         forms.CharField(required=True, min_length=2),),
                        ('last_name',
                         forms.CharField(required=True, min_length=2),)
                        ]
        fields = extra_fields + list(form_cls.declared_fields.viewitems())
        form_cls.base_fields = form_cls.declared_fields = OrderedDict(fields)

    def patch_view(self, view):
        def generate_username(s, form):
            c = form.cleaned_data
            username = populate_username(c['first_name'], c['last_name'])
            User = get_user_model()
            from account.utils import get_user_lookup_kwargs
            lookup_kwargs = get_user_lookup_kwargs({
                "{username}__iexact": username
            })
            qs = User.objects.filter(**lookup_kwargs)
            if not qs.exists():
                return username
            else:
                lookup_kwargs = get_user_lookup_kwargs({
                    "{username}__startswith": username
                })
                qs = User.objects.filter(**lookup_kwargs)
                username += '_{}'.format((qs.count()))
                try:
                    User.objects.get(username__iexact=username)
                except User.DoesNotExist:
                    return username
            raise forms.ValidationError(_("This username already exists."))

        view.generate_username = generate_username

    def on_signed_up(self, user, form, *args, **kwargs):
        user.first_name = ''.join(e for e in form.cleaned_data['first_name'] if e in string.ascii_letters or '-' == e)
        user.last_name = ''.join(e for e in form.cleaned_data['last_name'] if e in string.ascii_letters or '-' == e)
        user.save()
        form.cleaned_data['username'] = user.username

    def ready(self):
        from account.forms import SignupForm
        from account.views import SignupView
        from account.signals import user_signed_up

        self.patch_form(SignupForm)
        self.patch_view(SignupView)
        user_signed_up.connect(self.on_signed_up, sender=SignupForm)


default_app_config = 'ihp.IHPAppConfig'
