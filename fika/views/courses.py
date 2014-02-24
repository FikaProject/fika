from pyramid.view import view_config
from pyramid.view import view_defaults
from pyramid.httpexceptions import HTTPFound
from betahaus.pyracont.interfaces import IBaseFolder

from fika.views.base import BaseView
from fika.models.interfaces import ICourse
from fika.models.interfaces import ICourses
from fika.models.interfaces import IUser
from fika import security



@view_defaults(permission = security.VIEW)
class CourseView(BaseView):

    @view_config(context = ICourse, renderer = "fika:templates/course.pt")
    def course(self):
        course_modules = self.root['course_modules']
        results = []
        for name in self.context.get_field_value('course_modules', ()):
            results.append(course_modules[name])
        self.response['course_modules'] = results
        self.response['users'] = self.root['users']
        return self.response

    @view_config(context = ICourses, renderer = "fika:templates/courses.pt")
    def courses(self):
        self.response['courses'] = self.context.values()
        self.response['course_modules'] = self.root['course_modules']
        return self.response
    
    @view_config(context = ICourse, name = "join", renderer = "fika:templates/course.pt")
    def join(self):
        self.profile.join_course(self.context)
        return HTTPFound(location = self.request.resource_url(self.context))

    @view_config(context = ICourse, name = "leave", renderer = "fika:templates/course.pt")
    def leave(self):
        self.profile.leave_course(self.context)
        return HTTPFound(location = self.request.resource_url(self.context)) 
    
    # @view_config(context = IBaseFolder, name = "leave", renderer = "fika:templates/course.pt")
    # def leave(self):
    #     user = self.root['users'][self.userid]
    #     course = self.request.GET.get('course')
    #     user.get_field_value('courses', ()).remove(course)
    #     return HTTPFound(location = self.request.url)
    