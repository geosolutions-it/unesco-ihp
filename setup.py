import os
from distutils.core import setup

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name="ihp",
    version="0.1",
    author="",
    author_email="",
    description="ihp, based on GeoNode",
    long_description=(read('README.rst')),
    # Full list of classifiers can be found at:
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 1 - Planning',
    ],
    license="BSD",
    keywords="ihp geonode django",
    url='https://github.com/ihp/ihp',
    packages=['ihp'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'django-tastypie',
        # 'geonode==2.5.4',
        # 'celery==3.1.18',
        'elasticsearch==2.4.1',  # workaround since geonode doesn't fix version
        'geonode-user-messages',
        'pycountry',
        'photologue==3.7',  # later releases depend on django>=1.11
    ],

      dependency_links=[
        'https://github.com/GeoNode/geonode-user-messages/archive/master.zip#egg=geonode-user-messages-0.1.6',
      ]
)
