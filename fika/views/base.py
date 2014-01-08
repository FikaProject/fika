import deform
from js.deform import deform_basic
from js.deform import auto_need
from js.deform_bootstrap import deform_bootstrap_js
from js.bootstrap import bootstrap
from js.bootstrap import bootstrap_theme
from pyramid.view import view_config
from pyramid.decorator import reify
from pyramid.renderers import get_renderer
from pyramid.traversal import lineage
from betahaus.pyracont.interfaces import IContentFactory
from betahaus.pyracont.interfaces import IBaseFolder
from betahaus.pyracont.factories import createSchema
from pyramid.httpexceptions import HTTPForbidden
from pyramid.httpexceptions import HTTPFound

from fika.fanstatic import main_css


class BaseView(object):
    
    def __init__(self, context, request):
        self.context = context
        self.request = request
        deform_basic.need()
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

    def show_edit(self, context):
        if 'edit' in context.schemas:
            return True

    def breadcrumbs(self):
        return reversed(list(lineage(self.context)))


class BaseEdit(BaseView):

    @view_config(context = IBaseFolder, name = "add", renderer = "fika:templates/form.pt")
    def add(self):
        content_type = self.request.GET.get('content_type', '')
        factory = self.request.registry.queryUtility(IContentFactory, name = content_type)
        if not factory:
            return HTTPForbidden("No factory with that name")
        schema = createSchema(factory._callable.schemas['add'])
        schema = schema.bind(context = self.context, request = self.request, view = self)
        form = deform.Form(schema, buttons = ('save', 'cancel'))
        auto_need(form)
        if self.request.method == 'POST':
            if 'save' in self.request.POST:
                controls = self.request.POST.items()
                try:
                    appstruct = form.validate(controls)
                except deform.ValidationFailure, e:
                    self.response['form'] = e.render()
                    return self.response
                obj = factory(**appstruct)
                self.context[obj.uid] = obj
                return HTTPFound(location = self.request.resource_url(obj))
        self.response['form'] = form.render()
        return self.response

    @view_config(context = IBaseFolder, name = "edit", renderer = "fika:templates/form.pt")
    def edit(self):
        schema = createSchema(self.context.schemas['edit'])
        schema = schema.bind(context = self.context, request = self.request, view = self)
        form = deform.Form(schema, buttons = ('save', 'cancel'))
        auto_need(form)
        if self.request.method == 'POST':
            if 'save' in self.request.POST:
                controls = self.request.POST.items()
                try:
                    appstruct = form.validate(controls)
                except deform.ValidationFailure, e:
                    self.response['form'] = e.render()
                    return self.response
                self.context.set_field_appstruct(appstruct)
            return HTTPFound(location = self.request.resource_url(self.context))
        appstruct = self.context.get_field_appstruct(schema)
        self.response['form'] = form.render(appstruct = appstruct)
        return self.response


class DummyView(BaseView):

    @view_config(context = object, renderer = 'fika:templates/master.pt')
    def view(self):
        return self.response
