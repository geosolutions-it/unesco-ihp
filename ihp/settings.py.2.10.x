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

# Django settings for the GeoNode project.
import ast
import os
from urlparse import urlparse, urlunparse
# Load more settings from a file called local_settings.py if it exists
try:
    from ihp.local_settings import *
#    from geonode.local_settings import *
except ImportError:
    from geonode.settings import *

DEBUG = ast.literal_eval(os.getenv('DEBUG', 'False'))

#
# General Django development settings
#
PROJECT_NAME = 'ihp'

# add trailing slash to site url. geoserver url will be relative to this
if not SITEURL.endswith('/'):
    SITEURL = '{}/'.format(SITEURL)

SITENAME = os.getenv("SITENAME", 'ihp')

# Defines the directory that contains the settings file as the LOCAL_ROOT
# It is used for relative settings elsewhere.
LOCAL_ROOT = os.path.abspath(os.path.dirname(__file__))

WSGI_APPLICATION = "{}.wsgi.application".format(PROJECT_NAME)

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = os.getenv('LANGUAGE_CODE', "en")

if PROJECT_NAME not in INSTALLED_APPS:
    INSTALLED_APPS += ('photologue', 'sortedm2m', 'ihp', 'ihp.content', 'ihp.profile')

# Location of url mappings
ROOT_URLCONF = os.getenv('ROOT_URLCONF', '{}.urls'.format(PROJECT_NAME))

# Additional directories which hold static files
STATICFILES_DIRS.append(
    os.path.join(LOCAL_ROOT, "static"),
)

# Location of locale files
LOCALE_PATHS = (
    os.path.join(LOCAL_ROOT, 'locale'),
    ) + LOCALE_PATHS

TEMPLATES[0]['DIRS'].insert(0, os.path.join(LOCAL_ROOT, "templates"))
loaders = TEMPLATES[0]['OPTIONS'].get('loaders') or ['django.template.loaders.filesystem.Loader','django.template.loaders.app_directories.Loader']
# loaders.insert(0, 'apptemplates.Loader')
TEMPLATES[0]['OPTIONS']['loaders'] = loaders
TEMPLATES[0].pop('APP_DIRS', None)

CLIENT_RESULTS_LIMIT = 5
API_LIMIT_PER_PAGE = 1000
FREETEXT_KEYWORDS_READONLY = True
RESOURCE_PUBLISHING = True
ADMIN_MODERATE_UPLOADS = True
GROUP_PRIVATE_RESOURCES = True
GROUP_MANDATORY_RESOURCES = True
MODIFY_TOPICCATEGORY = True
USER_MESSAGES_ALLOW_MULTIPLE_RECIPIENTS = True
DISPLAY_WMS_LINKS = True
FAVORITE_ENABLED = False

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

AUTH_USER_MODEL = os.getenv('AUTH_USER_MODEL', 'profile.IHPProfile')

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
PINAX_NOTIFICATIONS_HOOKSET = "ihp.profile.hooks.IHPNotificationsHookSet"

# pinax.notifications
# or notification
NOTIFICATIONS_MODULE = 'pinax.notifications'

if NOTIFICATION_ENABLED and 'pinax.notifications' not in INSTALLED_APPS:
    INSTALLED_APPS += (NOTIFICATIONS_MODULE, )

# set to true to have multiple recipients in /message/create/
USER_MESSAGES_ALLOW_MULTIPLE_RECIPIENTS = True

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
            'level': 'DEBUG',
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
            "handlers": ["console"], "level": "DEBUG", },
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
API_LOCKDOWN = False
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

# Choose thumbnail generator -- this is the default generator
THUMBNAIL_GENERATOR = "geonode.layers.utils.create_gs_thumbnail_geonode"
# THUMBNAIL_GENERATOR_DEFAULT_BG = r"http://a.tile.openstreetmap.org/{z}/{x}/{y}.png"
# THUMBNAIL_GENERATOR_DEFAULT_BG = r"https://maps.wikimedia.org/osm-intl/{z}/{x}/{y}.png"
THUMBNAIL_GENERATOR_DEFAULT_BG = None

# Cache Bustin Settings
CACHE_BUSTING_STATIC_ENABLED = ast.literal_eval(os.environ.get('CACHE_BUSTING_STATIC_ENABLED', 'False'))
CACHE_BUSTING_MEDIA_ENABLED = ast.literal_eval(os.environ.get('CACHE_BUSTING_MEDIA_ENABLED', 'False'))

if not DEBUG and not S3_STATIC_ENABLED and not S3_MEDIA_ENABLED:
    if CACHE_BUSTING_STATIC_ENABLED or CACHE_BUSTING_MEDIA_ENABLED:
        from django.contrib.staticfiles import storage
        storage.ManifestStaticFilesStorage.manifest_strict = False
    if CACHE_BUSTING_STATIC_ENABLED:
        STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
    if CACHE_BUSTING_MEDIA_ENABLED:
        DEFAULT_FILE_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

