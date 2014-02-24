from __future__ import absolute_import

from fanstatic import Library
from fanstatic import Resource
from js.bootstrap import bootstrap
from js.jquery import jquery


lib_fika = Library("fika", "static")
main_css = Resource(lib_fika, 'main.css')
common_js = Resource(lib_fika, "common.js", depends = (jquery, bootstrap))
