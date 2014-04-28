import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

requires = [
    'Arche',
    'pyramid',
    #'betahaus.pyracont<=0.2b',
    'betahaus.viewcomponent',
    'colander',
    'deform',
    'pyramid_deform',
    'fanstatic',
    'lingua',
    'Babel',
    ]

setup(name='fika',
      version='0.1dev',
      description='fika',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Development Status :: 3 - Alpha",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Fika development team and contributors',
      author_email='robin@betahaus.net',
      url='https://github.com/FikaProject/fika',
      keywords='web pylons pyramid education e-learning',
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
      message_extractors = { '.': [
              ('**.py',   'lingua_python', None ),
              ('**.pt',   'lingua_xml', None ),
              ]},
      )
