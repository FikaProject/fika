from js.deform import deform
from js.deform_bootstrap import deform_bootstrap_js
from js.bootstrap import bootstrap
from js.bootstrap import bootstrap_theme
from pyramid.view import view_config

from fika.fanstatic import main_css


class BaseView(object):
    
    def __init__(self, context, request):
        deform.need()
        deform_bootstrap_js.need()
        bootstrap.need()
        bootstrap_theme.need()
        main_css.need()


class DummyView(BaseView):

    @view_config(context = object, renderer = 'fika:templates/master.pt')
    def view(self):
        return {}
