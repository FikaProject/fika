from hashlib import md5

import colander
import deform
from js.deform import deform_basic
from js.deform import auto_need
from js.deform_bootstrap import deform_bootstrap_js
from js.bootstrap import bootstrap_theme
from js.jqueryui import jqueryui
from pyramid.view import view_config
from pyramid.decorator import reify
from pyramid.renderers import get_renderer
from pyramid.traversal import lineage
from pyramid.traversal import find_root
from pyramid.security import authenticated_userid
from pyramid.security import forget
from pyramid.renderers import render
from betahaus.pyracont.interfaces import IContentFactory
from betahaus.pyracont.interfaces import IBaseFolder
from betahaus.pyracont.factories import createSchema
from pyramid.httpexceptions import HTTPForbidden
from pyramid.httpexceptions import HTTPFound
from pyramid.security import effective_principals

from fika.fanstatic import main_css
from fika.fanstatic import common_js
from fika.models.interfaces import IModuleSegment
from fika import FikaTSF as _
from fika import security


class BaseView(object):
    
    def __init__(self, context, request):
        self.context = context
        self.request = request
        deform_basic.need()
        deform_bootstrap_js.need()
        bootstrap_theme.need()
        main_css.need()
        jqueryui.need()
        common_js.need()
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

    @reify
    def root(self):
        return find_root(self.context)

    @reify
    def userid(self):
        return authenticated_userid(self.request)

    @reify
    def profile(self):
        profile = self.root['users'].get(self.userid, None)
        if self.userid and not profile:
            headers = forget(self.request)
            self.request.response.headerlist.extend(headers)
        return profile

    @property
    def roles_in_context(self):
        return effective_principals(self.request)

    def gravatar_link(self, size = 20):
        if not self.profile:
            return u''
        email = self.profile.default_email()
        if email:
            email_hash = md5(email.strip().lower()).hexdigest()
            return """<img src="https://secure.gravatar.com/avatar/%(hash)s?s=%(size)s" height="%(size)s" width="%(size)s" alt="" />""" % {'hash': email_hash, 'size': size}
        return u''

    def show_edit(self, context):
        if 'edit' in context.schemas:
            return True

    def breadcrumbs(self):
        return reversed(list(lineage(self.context)))

    def render_segment(self, segment):
        assert IModuleSegment.providedBy(segment)
        response = {}
        response.update(self.response)
        response['context'] = segment
        return render("fika:templates/segment.pt", response, request = self.request)


class BaseEdit(BaseView):

    @view_config(context = IBaseFolder, name = "add", renderer = "fika:templates/form.pt")
    def add(self):
        content_type = self.request.GET.get('content_type', '')
        factory = self.request.registry.queryUtility(IContentFactory, name = content_type)
        if not factory:
            return HTTPForbidden("No factory with that name")
        schema = createSchema(factory._callable.schemas['add'])
        schema = schema.bind(context = self.context, request = self.request, view = self)
        form = deform.Form(schema, buttons = ('save', 'cancel'), action="#")
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
            return HTTPFound(location = self.request.resource_url(self.context))
        self.response['form'] = form.render()
        return self.response

    @view_config(context = IBaseFolder, name = "edit", renderer = "fika:templates/form.pt",
                 permission = security.EDIT)
    def edit(self):
        schema = createSchema(self.context.schemas['edit'])
        schema = schema.bind(context = self.context, request = self.request, view = self)
        form = deform.Form(schema, buttons = ('save', 'cancel'), action="#")
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

    @view_config(context = IBaseFolder, name = "delete", renderer = "fika:templates/form.pt",
                 permission = security.DELETE)
    def delete(self):
        if self.context.__parent__ == None:
            raise HTTPForbidden(u"Can't delete root")
        schema = colander.Schema()
        schema = schema.bind(context = self.context, request = self.request, view = self)
        form = deform.Form(schema, buttons = ('delete', 'cancel'), action="#")
        auto_need(form)
        if self.request.method == 'POST':
            if 'delete' in self.request.POST:
                parent = self.context.__parent__
                del parent[self.context.__name__]
                return HTTPFound(location = self.request.resource_url(parent))
            return HTTPFound(location = self.request.resource_url(self.context))
        self.response['form'] = form.render()
        return self.response


class DummyView(BaseView):

    @view_config(context = object, renderer = 'fika:templates/home.pt')
    def view(self):
        self.response['users'] = self.root['users']
        self.response['courses'] = self.root['courses']
        return self.response
