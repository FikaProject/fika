How to update locales
=====================

These instructions expects you to use the 'py'-file in bin, created
when using buildout. Also, do source bin/activate to activate the local python
within your current bash shell. Then go to the eggs root dir with setup.py in it.

Further reading: http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/i18n.html

Extract messages & update catalog
---------------------------------

py setup.py extract_messages

Your .pot-file is now updated, make sure there were no error messages

py setup.py update_catalog

All locales (*.po) are now updated from the main .pot file.

Edit translations
-----------------

Within each language code directory, there are .po and .mo files.
The .mo-files are compiled, so you don't need to touch them.

Open the .po-files with an appropriate editor like POEdit.
Translate.
Save.

Compiling files
---------------

When you saved, the .mo-files should have been created. If not, run:

py setup.py compile_catalog

Testing
-------

After compilation, it's possible to test lang. Set language via

pyramid.default_locale_name = sv

In the used paster.ini file
