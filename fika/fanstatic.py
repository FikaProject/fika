from __future__ import absolute_import

from fanstatic import Library
from fanstatic import Resource
from js.bootstrap import bootstrap
from js.jquery import jquery

from arche.interfaces import (IBaseView,
                              IViewInitializedEvent)


lib_fika = Library("fika", "static")
main_css_fika = Resource(lib_fika, 'main.css')
common_js = Resource(lib_fika, "common.js", depends = (jquery, bootstrap))
lightbox_css = Resource(lib_fika, 'lightbox.css')
lightbox_js = Resource(lib_fika, 'lightbox.js', depends = (jquery, ), bottom=True)



def include_fika_resources(view, event):

    main_css_fika.need()



def includeme(config):

    config.add_subscriber(include_fika_resources, [IBaseView, IViewInitializedEvent])
