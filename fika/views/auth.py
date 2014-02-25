import deform
from pyramid.view import view_config
from pyramid.security import remember
from pyramid.security import forget
from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPFound
from betahaus.pyracont.factories import createContent
from betahaus.pyracont.factories import createSchema

from .base import BaseForm
from fika.models.interfaces import ISiteRoot
from fika.schemas.common import deferred_login_password_validator
from fika import FikaTSF as _


@view_config(context = ISiteRoot, name = "login", renderer = "fika:templates/form.pt")
class LoginForm(BaseForm):

    @property
    def buttons(self):
        #FIXME: Forgot password here!
        return (deform.Button('login', title = _(u"Login"), css_class = 'btn btn-default'), self.button_cancel,)

    @reify
    def schema(self):
        schema = createSchema('LoginSchema')
        schema.validator = deferred_login_password_validator
        return schema

    def login_success(self, appstruct):
        self.flash_messages.add(_(u"Welcome!"), type="success")
        user = self.root['users'].get_user_by_email(appstruct['email'])
        headers = remember(self.request, user.uid)
        return HTTPFound(location = self.request.application_url, headers = headers)


@view_config(context = ISiteRoot, name = "register", renderer = "fika:templates/form.pt")
class RegisterForm(BaseForm):

    @property
    def buttons(self):
        return (deform.Button('register', title = _(u"Register"), css_class = 'btn btn-default'), self.button_cancel,)

    @reify
    def schema(self):
        return createSchema('RegisterSchema')

    def register_success(self, appstruct):
        self.flash_messages.add(_(u"Welcome, you're now registered!"), type="success")
        obj = createContent('User', **appstruct)
        self.context['users'][obj.uid] = obj
        headers = remember(self.request, obj.uid)
        return HTTPFound(location = self.request.application_url, headers = headers)


@view_config(context = ISiteRoot, name = "logout")
def logout(context, request):
    headers = forget(request)
    return HTTPFound(location = request.resource_url(context),
                     headers = headers)
