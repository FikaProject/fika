from __future__ import absolute_import

from fanstatic import Library
from fanstatic import Resource


lib_fika = Library("fika", "static")
main_css = Resource(lib_fika, 'main.css')
