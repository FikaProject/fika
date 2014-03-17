import deform
from js.deform import auto_need
from pyramid.view import view_config
from pyramid.view import view_defaults
from pyramid.httpexceptions import HTTPFound
from betahaus.pyracont.factories import createSchema

from fika import security
from fika.views.base import BaseView
from fika.models.interfaces import IUser
from fika.models.interfaces import IUsers

@view_defaults(permission = security.VIEW)
class UsersView(BaseView):

    @view_config(context = IUsers, renderer = "fika:templates/users.pt")
    def users(self):
        self.response['users'] = self.context.values()
        #import pdb; pdb.set_trace()
        return self.response

    @view_config(context = IUser, renderer = "fika:templates/user.pt")
    def user(self):
        self.response['courses'] = self.root['courses']
        return self.response

    @view_config(context = IUser, name = "change_password", renderer = "fika:templates/form.pt")
    def change_password(self):
        schema = createSchema('ChangeUserPasswordSchema')
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
        self.response['form'] = form.render()
        return self.response
    
    @view_config(context = IUser, name = "leave", renderer = "fika:templates/course.pt")
    def leave(self):
        user = self.root['users'][self.userid]
        course = self.request.GET.get('course')
        user.get_field_value('courses', ()).remove(course)
        return HTTPFound(location = self.request.resource_url(user))
