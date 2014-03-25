from hashlib import md5

import deform
from js.deform import deform_basic
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
from pyramid.security import effective_principals
from pyramid.httpexceptions import HTTPForbidden
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import render
from pyramid_deform import FormView
from betahaus.pyracont.interfaces import IContentFactory
from betahaus.pyracont.interfaces import IBaseFolder
from betahaus.pyracont.factories import createSchema
from betahaus.viewcomponent import render_view_group

from fika.fanstatic import main_css
from fika.fanstatic import common_js
from fika.models.interfaces import IMediaObject
from fika.models.interfaces import ISecurityAware
from fika.models.flash_messages import get_flash_messages
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
        self.main_title = request.registry.settings.get('fika.main_title', u'Fika')

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

    @reify
    def flash_messages(self):
        return get_flash_messages(self.request)

    @property
    def roles_in_context(self):
        return effective_principals(self.request)

    def gravatar_image(self, email, size = 30, tags = None, gravatar_opts = None):
        if email:
            email_hash = md5(email.strip().lower()).hexdigest()
            #Gravatar options
            default_gravatar = {'size': size,
                                'd': 'retro',}
            if gravatar_opts:
                default_gravatar.update(tags)
            #Tag options
            default_tags = {'height': size,
                            'width': size,
                            'alt': '',
                            'class': 'profile-image',
                            }
            if tags:
                default_tags.update(tags)
            out = u'<img src="https://secure.gravatar.com/avatar/%s?' % email_hash
            out += "&".join(["%s=%s" % (k, v) for (k, v) in default_gravatar.items()])
            out += '"'
            out += " ".join(['%s="%s"' % (k, v) for (k, v) in default_tags.items()])
            out += ' />'
            return out
        return u''

    def context_has_permission(self, context, permission):
        return security.context_has_permission(context, permission, userid = self.userid)

    def show_edit(self, context):
        if 'edit' in context.schemas:
            return True

    def breadcrumbs(self):
        return reversed(list(lineage(self.context)))

    def render_action_bar(self, context):
        response = {}
        response.update(self.response)
        response['context'] = context
        response['actions'] = render_view_group(context, self.request, 'actions', view = self)
        return render("fika:templates/action_bar.pt", response, request = self.request)

    def render_media_object(self, mediaObject):
        assert IMediaObject.providedBy(mediaObject)
        response = {}
        response.update(self.response)
        response['context'] = mediaObject
        return render("fika:templates/media_object.pt", response, request = self.request)


class BaseForm(BaseView, FormView):
    default_success = _(u"Done")
    default_cancel = _(u"Canceled")

    button_delete = deform.Button('delete', title = _(u"Delete"), css_class = 'btn btn-danger')
    button_cancel = deform.Button('cancel', title = _(u"Cancel"), css_class = 'btn btn-default')
    button_save = deform.Button('save', title = _(u"Save"), css_class = 'btn btn-primary')
    button_add = deform.Button('add', title = _(u"Add"), css_class = 'btn btn-primary')

    @property
    def form_options(self):
        return {'action': self.request.url}

    def get_bind_data(self):
        return {'context': self.context, 'request': self.request, 'view': self}

    def appstruct(self):
        if self.schema:
            return self.context.get_field_appstruct(self.schema)

    def cancel(self, *args):
        self.flash_messages.add(self.default_cancel)
        return HTTPFound(location = self.request.resource_url(self.context))
    cancel_success = cancel_failure = cancel


@view_config(context = IBaseFolder, name = "edit", renderer = "fika:templates/form.pt", permission = security.EDIT)
class DefaultEdit(BaseForm):

    @property
    def buttons(self):
        return (self.button_save, self.button_cancel,)

    @reify
    def schema(self):
        return createSchema(self.context.schemas['edit'])

    def save_success(self, appstruct):
        self.flash_messages.add(self.default_success, type="success")
        self.context.set_field_appstruct(appstruct)
        return HTTPFound(location = self.request.resource_url(self.context))


@view_config(context = IBaseFolder, name = "add", renderer = "fika:templates/form.pt")
class DefaultAdd(BaseForm):

    @property
    def buttons(self):
        return (self.button_add, self.button_cancel,)

    def __call__(self):
        #FIXME: Check add permission here...
        return super(DefaultAdd, self).__call__()

    def appstruct(self):
        return {}

    @reify
    def factory(self):
        content_type = self.request.GET.get('content_type', '')
        factory = self.request.registry.queryUtility(IContentFactory, name = content_type)
        if not factory:
            raise HTTPForbidden("No factory with that name")
        return factory

    @reify
    def schema(self):
        return createSchema(self.factory._callable.schemas['add'])

    def add_success(self, appstruct):
        obj = self.factory(**appstruct)
        self.context[obj.uid] = obj
        self.flash_messages.add(self.default_success, type="success")
        return HTTPFound(location = self.request.resource_url(obj))


@view_config(context = IBaseFolder, name = "add", renderer = "fika:templates/form.pt",
             request_param = "content_type=File")
class AddFileForm(DefaultAdd):
    
    def add_success(self, appstruct):
        kwargs = appstruct['file']
        obj = self.factory(**kwargs)
        name = appstruct['file']['filename']
        #XXX validate name
        self.context[name] = obj
        self.flash_messages.add(self.default_success, type="success")
        return HTTPFound(location = self.request.resource_url(obj))


@view_config(context = ISecurityAware, name = "delete", renderer = "fika:templates/form.pt",
             permission = security.DELETE)
class DefaultDelete(BaseForm):

    def appstruct(self):
        return {}

    @property
    def buttons(self):
        return (self.button_delete, self.button_cancel,)

    @reify
    def schema(self):
        if 'delete' in self.context.schemas:
            return createSchema(self.context.schemas['delete'])

    def delete_success(self, appstruct):
        parent = self.context.__parent__
        del parent[self.context.__name__]
        self.flash_messages.add(self.default_success, type="success")
        return HTTPFound(location = self.request.resource_url(parent))


class DummyView(BaseView):

    @view_config(context = object, renderer = 'fika:templates/home.pt')
    def view(self):
        self.response['users'] = self.root['users']
        self.response['courses'] = self.root['courses']
        self.response['course_modules'] = self.root['course_modules']
        return self.response


class OrderView(BaseView):
    
    @view_config(name = 'order', context = IBaseFolder, permission = security.EDIT, renderer = "fika:templates/ordering.pt")
    def ordering(self):
        #FIXME not done! This view needs to write the keys within this context to context.order
        return self.response
