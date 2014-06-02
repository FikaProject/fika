from arche.interfaces import IUser
from arche.views.base import BaseView
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from pyramid.view import view_defaults

from fika import security


@view_defaults(permission = security.VIEW)
class UsersView(BaseView):

    @view_config(context = IUser, renderer = "fika:templates/user.pt")
    def user(self):
        self.response['courses'] = self.root['courses']
        return self.response
    
    @view_config(context = IUser, name = "leave", renderer = "fika:templates/course.pt")
    def leave(self):
        user = self.root['users'][self.userid]
        course = self.request.GET.get('course')
        user.get_field_value('courses', ()).remove(course)
        return HTTPFound(location = self.request.resource_url(user))
