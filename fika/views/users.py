from pyramid.view import view_config

from fika.views.base import BaseView
from fika.models.interfaces import IUser
from fika.models.interfaces import IUsers


class UsersView(BaseView):

    @view_config(context = IUsers, renderer = "fika:templates/users.pt")
    def users(self):
        self.response['users'] = self.context.values()
        return self.response

    @view_config(context = IUser, renderer = "fika:templates/user.pt")
    def user(self):
        return self.response
