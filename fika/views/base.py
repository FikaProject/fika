from js.deform import deform
from js.deform_bootstrap import deform_bootstrap_js
from js.bootstrap import bootstrap
from js.bootstrap import bootstrap_theme
from pyramid.view import view_config
from pyramid.decorator import reify
from pyramid.renderers import get_renderer
from betahaus.pyracont.interfaces import IContentFactory
from pyramid.httpexceptions import HTTPForbidden

from fika.fanstatic import main_css


class BaseView(object):
    
    def __init__(self, context, request):
        self.context = context
        self.request = request
        deform.need()
        deform_bootstrap_js.need()
        bootstrap.need()
        bootstrap_theme.need()
        main_css.need()
        self.response = {'view': self}

    @property
    def addable_types(self):
        addable = []
        for (name, factory) in self.request.registry.getUtilitiesFor(IContentFactory):
            for iface in factory._callable.allowed_contexts:
                if iface.providedBy(self.context):
                    addable.append(name)
                    break
        return addable


    @reify
    def main_macro(self):
        return get_renderer('fika:templates/master.pt').implementation().macros['main']



class BaseEdit(BaseView):

    @view_config(context = object, name = "add", renderer = "fika:templates/form.pt")
    def add(self):
        content_type = self.request.GET.get('content_type', '')
        factory = self.request.registry.queryUtility(IContentFactory, name = content_type)
        if not factory:
            return HTTPForbidden("No factory with that name")
        
        return self.response


class DummyView(BaseView):

    @view_config(context = object, renderer = 'fika:templates/master.pt')
    def view(self):
        return self.response
