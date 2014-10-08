from arche import security
from arche.interfaces import IUser
from arche.views.base import BaseView
from fika.views.fika_base_view import FikaBaseView
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from pyramid.view import view_defaults


@view_defaults(permission = security.PERM_VIEW)
class UsersView(FikaBaseView):
    
    def __init__(self, context, request):
        super(UsersView, self).__init__(context, request)
        self.response = {}

    @view_config(context = IUser, renderer = "fika:templates/user.pt")
    def user(self):
        self.response['courses'] = self.root['courses']
        return self.response
