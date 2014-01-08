from pyramid.view import view_config

from fika.views.base import BaseView
from fika.models.interfaces import ICourseModule
from fika.models.interfaces import ICourseModules
from fika.models.interfaces import IModuleSegment


class CourseModulesView(BaseView):

    @view_config(context = ICourseModules, renderer = "fika:templates/course_modules.pt")
    def course_modules(self):
        self.response['course_modules'] = self.context.values()
        return self.response

    @view_config(context = ICourseModule, renderer = "fika:templates/course_module.pt")
    def course_module(self):
        self.response['module_segments'] = self.context.values()
        self.response['used_in_courses'] = self.root['courses'].module_used_in(self.context.uid)
        return self.response

    @view_config(context = IModuleSegment, renderer = "fika:templates/form.pt")
    def module_segment(self):
        self.response['form'] = self.context.render(self.request, self)
        return self.response
