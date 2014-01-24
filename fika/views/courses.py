from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from fika.views.base import BaseView
from fika.models.interfaces import ICourse
from fika.models.interfaces import ICourses


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
        user = self.root['users'][self.userid]
        
        user.set_field_value('courses', user.get_field_value('courses', ()).__add__([self.context.uid]))
        return HTTPFound(location = self.request.resource_url(self.context))