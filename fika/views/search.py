from pyramid.view import view_config
from pyramid.view import view_defaults
from pyramid.httpexceptions import HTTPFound
from betahaus.pyracont.interfaces import IBaseFolder

from fika.views.base import BaseView
from fika.models.interfaces import ISiteRoot
from fika.models.interfaces import ICourses
from fika.models.interfaces import IUser
from fika import security



@view_defaults(permission = security.VIEW)
class SearchView(BaseView):

    @view_config(context =ISiteRoot, name = "search", renderer = "fika:templates/search.pt")
    def dummySearch(self):
        self.response['courses'] = self.context.values()
        self.response['course_modules'] = self.root['course_modules']
        return self.response