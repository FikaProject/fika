from pyramid.view import view_config

from fika.views.base import BaseView
from fika.models.interfaces import ICourseModules

class CourseModulesView(BaseView):

    @view_config(context = ICourseModules, renderer = "fika:templates/course_modules.pt")
    def course_modules(self):
        self.response['course_modules'] = self.context.values()
        return self.response
