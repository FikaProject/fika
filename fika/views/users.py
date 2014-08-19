from arche import security
from arche.interfaces import IUser
from arche.views.base import BaseView
from fika.models.interfaces import IFikaUser
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from pyramid.view import view_defaults


@view_defaults(permission = security.PERM_VIEW)
class UsersView(BaseView):
    
    def __init__(self, context, request):
        super(UsersView, self).__init__(context, request)
        self.response = {}

    @view_config(context = IUser, renderer = "fika:templates/user.pt")
    def user(self):
        
        def _get_first_unfinished_page(courseuid):
            course = self.resolve_uid(courseuid)
            
            noModulesCompleted = True
            for uid in course.course_modules:
                if uid in self.profile.completed_course_modules:
                    noModulesCompleted = False
                    break
            if noModulesCompleted:
                return 0
            
            for uid in course.course_modules:
                if uid not in self.profile.completed_course_modules:
                    for (k,v) in course.cm_pages().items():
                        if v == uid:
                            return k
            return 0
        
        self.response['courses'] = self.root['courses']
        user = self.root['users'].get(self.request.authenticated_userid, None)
        if user:
            self.response['fikaProfile'] = IFikaUser(user)
            
        self.response['get_first_unfinished_page'] = _get_first_unfinished_page
        return self.response
    
    @view_config(context = IUser, name = "leave", renderer = "fika:templates/course.pt")
    def leave(self):
        user = self.root['users'][self.userid]
        course = self.request.GET.get('course')
        user.get_field_value('courses', ()).remove(course)
        return HTTPFound(location = self.request.resource_url(user))
