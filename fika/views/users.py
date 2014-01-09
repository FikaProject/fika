import deform
from js.deform import auto_need
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from betahaus.pyracont.factories import createSchema

from fika.views.base import BaseView
from fika.models.interfaces import IUser
from fika.models.interfaces import IUsers
from fika.schemas.common import deferred_login_password_validator


class UsersView(BaseView):

    @view_config(context = IUsers, renderer = "fika:templates/users.pt")
    def users(self):
        self.response['users'] = self.context.values()
        return self.response

    @view_config(context = IUser, renderer = "fika:templates/user.pt")
    def user(self):
        return self.response

    @view_config(context = IUser, name = "change_password", renderer = "fika:templates/form.pt")
    def change_password(self):
        schema = createSchema('ChangeUserPasswordSchema')
        schema.validator = deferred_login_password_validator
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
        self.response['form'] = form.render()
        return self.response
