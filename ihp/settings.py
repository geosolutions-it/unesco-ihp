# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2012 OpenPlans
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

# Django settings for the GeoNode project.

import os

# Load more settings from a file called local_settings.py if it exists
try:
    from ihp.local_settings import *
#    from geonode.local_settings import *
except ImportError:
    from geonode.settings import *


DEBUG = False

#
# General Django development settings
#
SITENAME = 'ihp'

# Defines the directory that contains the settings file as the LOCAL_ROOT
# It is used for relative settings elsewhere.
LOCAL_ROOT = os.path.abspath(os.path.dirname(__file__))

WSGI_APPLICATION = "ihp.wsgi.application"

# Additional directories which hold static files
STATICFILES_DIRS.insert(0, os.path.join(LOCAL_ROOT, "static"))

# Note that Django automatically includes the "templates" dir in all the
# INSTALLED_APPS, se there is no need to add maps/templates or admin/templates
TEMPLATES[0]['DIRS'].insert(0, os.path.join(LOCAL_ROOT, "templates"))
TEMPLATES[0]['OPTIONS']['debug'] = True

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
#         'LOCATION': '/var/tmp/django_cache',
#     }
# }

# If you want to enable Mosaics use the following configuration
UPLOADER = {
    # 'BACKEND': 'geonode.rest',
    'BACKEND': 'geonode.importer',
    'OPTIONS': {
        'TIME_ENABLED': True,
        'MOSAIC_ENABLED': False,
        'GEOGIG_ENABLED': False,
    },
    'SUPPORTED_CRS': [
        'EPSG:4326',
        'EPSG:3785',
        'EPSG:3857',
        'EPSG:900913',
        'EPSG:32647',
        'EPSG:32736'
    ]
}

INSTALLED_APPS += ('photologue', 'sortedm2m', 'ihp', 'ihp.content')

# Location of url mappings
ROOT_URLCONF = 'ihp.urls'

# Location of locale files
LOCALE_PATHS = (
    os.path.join(LOCAL_ROOT, 'locale'),
    ) + LOCALE_PATHS

#RISKS = {'DEFAULT_LOCATION': 'AF',
#         'PDF_GENERATOR': {'NAME': 'weasyprint_api',
#                           #'NAME': 'wkhtml2pdf',
#                           'BIN': '/usr/bin/xvfb-run /usr/bin/wkhtmltopdf',
#                           'ARGS': []}}

CLIENT_RESULTS_LIMIT = 20
API_LIMIT_PER_PAGE = 1000
FREETEXT_KEYWORDS_READONLY = True
RESOURCE_PUBLISHING = True
ADMIN_MODERATE_UPLOADS = True
GROUP_PRIVATE_RESOURCES = True
GROUP_MANDATORY_RESOURCES = True
MODIFY_TOPICCATEGORY = True
USER_MESSAGES_ALLOW_MULTIPLE_RECIPIENTS = True
DISPLAY_WMS_LINKS = True

TIME_ZONE = 'Europe/Paris'

LANGUAGES = (
    ('en', "English"),
    ('fr', "Français"),
)

LICENSES = {
    'ENABLED': True,
    'DETAIL': 'never',
    'METADATA': 'never',
}

# prevent signing up by default
ACCOUNT_OPEN_SIGNUP = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_SUBJECT_PREFIX = ""
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_EMAIL_CONFIRMATION_EMAIL = True
ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = True
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_APPROVAL_REQUIRED = True

ACCOUNT_ADAPTER = 'ihp.content.adapters.UnescoLocalAccountAdapter'

SOCIALACCOUNT_ADAPTER = 'geonode.people.adapters.SocialAccountAdapter'

ACCOUNT_FORMS = {
    "signup": "ihp.content.forms.UnescoLocalAccountSignupForm",
}

SOCIALACCOUNT_AUTO_SIGNUP = False
SOCIALACCOUNT_FORMS = {
    "signup": "ihp.content.forms.UnescoSocialAccountSignupForm",
}
INSTALLED_APPS += (
    'allauth.socialaccount.providers.linkedin_oauth2',
    'allauth.socialaccount.providers.facebook',
)

SOCIALACCOUNT_PROVIDERS = {
    'linkedin_oauth2': {
        'SCOPE': [
            'r_emailaddress',
            'r_basicprofile',
        ],
        'PROFILE_FIELDS': [
            'emailAddress',
            'firstName',
            'headline',
            'id',
            'industry',
            'lastName',
            'pictureUrl',
            'positions',
            'publicProfileUrl',
            'location',
            'specialties',
            'summary',
        ]
    },
    'facebook': {
        'METHOD': 'oauth2',
        'SCOPE': [
            'email',
            'public_profile',
        ],
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'verified',
            'locale',
            'timezone',
            'link',
            'gender',
        ]
    },
}

SOCIALACCOUNT_PROFILE_EXTRACTORS = {
    "facebook": "geonode.people.profileextractors.FacebookExtractor",
    "linkedin_oauth2": "ihp.content.profileextractors.LinkedInExtractor",
}

# MAPs and Backgrounds

ALT_OSM_BASEMAPS = os.environ.get('ALT_OSM_BASEMAPS', False)
CARTODB_BASEMAPS = os.environ.get('CARTODB_BASEMAPS', False)
STAMEN_BASEMAPS = os.environ.get('STAMEN_BASEMAPS', False)
THUNDERFOREST_BASEMAPS = os.environ.get('THUNDERFOREST_BASEMAPS', False)
# MAPBOX_ACCESS_TOKEN = <defined on local_settings>
BING_API_KEY = os.environ.get('BING_API_KEY', None)

MAP_BASELAYERS = [{
    "source": {"ptype": "gxp_olsource"},
    "type": "OpenLayers.Layer",
    "args": ["No background"],
    "name": "background",
    "visibility": False,
    "fixed": True,
    "group":"background"
}, {
    "source": {"ptype": "gxp_olsource"},
    "type": "OpenLayers.Layer.XYZ",
    "title": "UNESCO",
    "args": ["UNESCO", "http://en.unesco.org/tiles/${z}/${x}/${y}.png"],
    "wrapDateLine": True,
    "name": "background",
    "attribution": "&copy; UNESCO",
    "visibility": False,
    "fixed": True,
    "group":"background"
}, {
    "source": {"ptype": "gxp_olsource"},
    "type": "OpenLayers.Layer.XYZ",
    "title": "UNESCO GEODATA",
    "args": ["UNESCO GEODATA", "http://en.unesco.org/tiles/geodata/${z}/${x}/${y}.png"],
    "name": "background",
    "attribution": "&copy; UNESCO",
    "visibility": False,
    "wrapDateLine": True,
    "fixed": True,
    "group":"background"
}, {
    "source": {"ptype": "gxp_olsource"},
    "type": "OpenLayers.Layer.XYZ",
    "title": "Humanitarian OpenStreetMap",
    "args": ["Humanitarian OpenStreetMap", "http://a.tile.openstreetmap.fr/hot/${z}/${x}/${y}.png"],
    "name": "background",
    "attribution": "&copy; <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a>, Tiles courtesy of <a href='http://hot.openstreetmap.org/' target='_blank'>Humanitarian OpenStreetMap Team</a>",
    "visibility": False,
    "wrapDateLine": True,
    "fixed": True,
    "group":"background"
}, {
    "source": {"ptype": "gxp_olsource"},
    "type": "OpenLayers.Layer.XYZ",
    "title": "MapBox Satellite Streets",
    "args": ["MapBox Satellite Streets", "http://api.mapbox.com/styles/v1/mapbox/satellite-streets-v9/tiles/${z}/${x}/${y}?access_token="+MAPBOX_ACCESS_TOKEN],
    "name": "background",
    "attribution": "&copy; <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> &copy; <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <a href='https://www.mapbox.com/feedback/' target='_blank'>Improve this map</a>",
    "visibility": False,
    "wrapDateLine": True,
    "fixed": True,
    "group":"background"
}, {
    "source": {"ptype": "gxp_olsource"},
    "type": "OpenLayers.Layer.XYZ",
    "title": "MapBox Streets",
    "args": ["MapBox Streets", "http://api.mapbox.com/styles/v1/mapbox/streets-v9/tiles/${z}/${x}/${y}?access_token="+MAPBOX_ACCESS_TOKEN],
    "name": "background",
    "attribution": "&copy; <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> &copy; <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <a href='https://www.mapbox.com/feedback/' target='_blank'>Improve this map</a>",
    "visibility": False,
    "wrapDateLine": True,
    "fixed": True,
    "group":"background"
}, {
    "source": {"ptype": "gxp_osmsource"},
    "type": "OpenLayers.Layer.OSM",
    "title": "OpenStreetMap",
    "name": "mapnik",
    "attribution": "&copy; <a href='http://osm.org/copyright'>OpenStreetMap</a> contributors",
    "visibility": True,
    "wrapDateLine": True,
    "fixed": True,
    "group": "background"
}]


if 'geonode.geoserver' in INSTALLED_APPS:
    LOCAL_GEOSERVER = {
        "source": {
            "ptype": "gxp_wmscsource",
            "url": OGC_SERVER['default']['PUBLIC_LOCATION'] + "wms",
            "restUrl": "/gs/rest"
        }
    }
    baselayers = MAP_BASELAYERS
    MAP_BASELAYERS = [LOCAL_GEOSERVER]
    MAP_BASELAYERS.extend(baselayers)

# notification settings
NOTIFICATION_ENABLED = True
# PINAX_NOTIFICATIONS_LANGUAGE_MODEL = "allauth.account.Account"

# notifications backends
_EMAIL_BACKEND = "pinax.notifications.backends.email.EmailBackend"
PINAX_NOTIFICATIONS_BACKENDS = [
    ("email", _EMAIL_BACKEND),
]

# Queue non-blocking notifications.
PINAX_NOTIFICATIONS_QUEUE_ALL = False
PINAX_NOTIFICATIONS_LOCK_WAIT_TIMEOUT = -1

# PINAX_NOTIFICATIONS_HOOKSET = "pinax.notifications.hooks.DefaultHookSet"
NOTIFICATIONS_ENABLED_BY_DEFAULT = False
PINAX_NOTIFICATIONS_HOOKSET = "geonode.people.hooks.IHPNotificationsHookSet"

# pinax.notifications
# or notification
NOTIFICATIONS_MODULE = 'pinax.notifications'

if NOTIFICATION_ENABLED and 'pinax.notifications' not in INSTALLED_APPS:
    INSTALLED_APPS += (NOTIFICATIONS_MODULE, )

# set to true to have multiple recipients in /message/create/
USER_MESSAGES_ALLOW_MULTIPLE_RECIPIENTS = True

MONITORING_ENABLED = True
if MONITORING_ENABLED:
    if 'geonode.contrib.monitoring' not in INSTALLED_APPS:
        INSTALLED_APPS += ('geonode.contrib.monitoring',)
    if 'geonode.contrib.monitoring.middleware.MonitoringMiddleware' not in MIDDLEWARE_CLASSES:
        MIDDLEWARE_CLASSES += ('geonode.contrib.monitoring.middleware.MonitoringMiddleware',)
    MONITORING_CONFIG = None
    MONITORING_HOST_NAME = 'ihp-wins-dev.geo-solutions.it'
    MONITORING_SERVICE_NAME = 'local-geonode'

if 'geonode.contrib.ows_api' not in INSTALLED_APPS:
    INSTALLED_APPS += ('geonode.contrib.ows_api',)

# GEOIP_PATH = "/usr/local/share/GeoIP"
GEOIP_PATH = os.path.join(os.path.dirname(__file__), '..', 'GeoLiteCity.dat')

UNOCONV_ENABLE = True

if UNOCONV_ENABLE:
   UNOCONV_EXECUTABLE = '/usr/bin/unoconv'
   UNOCONV_TIMEOUT = 60  # seconds

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d '
                      '%(thread)d %(message)s'
        },
        'simple': {
            'format': '%(message)s',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'INFO', 'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    "loggers": {
        "django": {
            "handlers": ["console"], "level": "INFO", },
        "geonode": {
            "handlers": ["console"], "level": "INFO", },
        "gsconfig.catalog": {
            "handlers": ["console"], "level": "INFO", },
        "owslib": {
            "handlers": ["console"], "level": "INFO", },
        "pycsw": {
            "handlers": ["console"], "level": "INFO", },
        "ihp": {
            "handlers": ["console"], "level": "DEBUG", },
        },
    }

# Security stuff
MIDDLEWARE_CLASSES += ('django.middleware.security.SecurityMiddleware',)
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = False
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
