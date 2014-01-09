from pyramid.view import view_config

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
        return self.response

    @view_config(context = ICourses, renderer = "fika:templates/courses.pt")
    def courses(self):
        self.response['courses'] = self.context.values()
        return self.response