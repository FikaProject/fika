import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'pyramid_zodbconn',
    'transaction',
    'pyramid_tm',
    'ZODB3',
    'betahaus.pyracont',
    'colander',
    'deform',
    'deform_bootstrap',
    'pyramid_deform',
    'fanstatic',
    'js.deform',
    'js.bootstrap',
    'js.deform_bootstrap',
    'js.jquery',
    'js.jqueryui',
    'js.jquery_timepicker_addon',
    'js.jquery_form',
    'js.jquery_maskedinput',
    'js.jquery_maskmoney',
    'js.tinymce',
    ]

setup(name='fika',
      version='0.1dev',
      description='fika',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="fika",
      entry_points="""\
      [paste.app_factory]
      main = fika:main
      [fanstatic.libraries]
      fika = fika.fanstatic:lib_fika
      """,
      )
