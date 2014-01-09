import deform
from pyramid.view import view_config
from pyramid.security import remember
from pyramid.security import forget
from js.deform import auto_need
#from pyramid.httpexceptions import HTTPForbidden
from pyramid.httpexceptions import HTTPFound
from betahaus.pyracont.factories import createContent
from betahaus.pyracont.factories import createSchema

from .base import BaseView
from fika.models.interfaces import ISiteRoot


class AuthView(BaseView):
    
    @view_config(context = ISiteRoot, name = "register", renderer = "fika:templates/form.pt")
    def register(self):
        schema = createSchema('RegisterUserSchema')
        schema = schema.bind(context = self.context, request = self.request, view = self)
        form = deform.Form(schema, buttons = ('register', 'cancel'))
        auto_need(form)
        if self.request.method == 'POST':
            if 'register' in self.request.POST:
                controls = self.request.POST.items()
                try:
                    appstruct = form.validate(controls)
                except deform.ValidationFailure, e:
                    self.response['form'] = e.render()
                    return self.response
                appstruct['email'] = list(appstruct['email'])
                obj = createContent('User', **appstruct)
                self.context['users'][obj.uid] = obj
                headers = remember(self.request, obj.uid)
                return HTTPFound(location = self.request.resource_url(obj),
                                 headers = headers)
            return HTTPFound(location = self.request.resource_url(self.context))
        self.response['form'] = form.render()
        return self.response

    @view_config(context = ISiteRoot, name = "login", renderer = "fika:templates/form.pt")
    def login(self):
        schema = createSchema('LoginSchema')
        schema = schema.bind(context = self.context, request = self.request, view = self)
        form = deform.Form(schema, buttons = ('login', 'cancel'))
        auto_need(form)
        if self.request.method == 'POST':
            if 'login' in self.request.POST:
                controls = self.request.POST.items()
                try:
                    appstruct = form.validate(controls)
                except deform.ValidationFailure, e:
                    self.response['form'] = e.render()
                    return self.response
                #Validation is handled by the schema
                user = self.root['users'].get_user_by_email(appstruct['email'], validated = True)
                headers = remember(self.request, user.uid)
                return HTTPFound(location = self.request.resource_url(user),
                                 headers = headers)
            return HTTPFound(location = self.request.resource_url(self.context))
        self.response['form'] = form.render()
        return self.response

    @view_config(context = ISiteRoot, name = "logout")
    def logout(self):
        headers = forget(self.request)
        return HTTPFound(location = self.request.resource_url(self.context),
                         headers = headers)
