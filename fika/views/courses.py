from pyramid.view import view_config
from pyramid.view import view_defaults
from pyramid.renderers import render
from pyramid.security import Allowed
from pyramid.httpexceptions import HTTPFound

from arche import security

from fika.views.fika_base_view import FikaBaseView
from fika.models.interfaces import ICourse
from fika.models.interfaces import ICourseModule
from fika.models.interfaces import ICourses
from fika.views.course_pagination import render_course_pagination

@view_defaults(permission = security.PERM_VIEW)
class CourseView(FikaBaseView):
    
    def __init__(self, context, request):
        super(CourseView, self).__init__(context, request)
        self.response = {}

    @view_config(context = ICourse, renderer = "fika:templates/course.pt", permission=security.PERM_VIEW)
    def course(self):
        self.response['course_modules'] = self.context.values()
        self.response['in_course'] = self.fikaProfile.in_course(self.context)
        self.response['course_pagination'] = render_course_pagination
        
        self.response['course_modules_media'] = {}
        for course_module in self.response['course_modules']:
            self.response['course_modules_media'][course_module.uid] = {}
            for segment in course_module.values():
                for media in segment.values():
                    if not hasattr(media, 'icon'):
                        continue
                    if media.icon in self.response['course_modules_media'][course_module.uid]:
                        self.response['course_modules_media'][course_module.uid][media.icon] += 1
                    else:
                        self.response['course_modules_media'][course_module.uid][media.icon] = 1
        return self.response
    
    @view_config(context = ICourses, renderer = "fika:templates/courses.pt", permission=security.PERM_VIEW)
    def courses(self):
        self.response['courses'] = self.context.values()
        self.response['can_create_course'] = False;
        if self.request.has_permission(security.PERM_EDIT, self.context):
            self.response['can_create_course'] = True;
        return self.response
    
    @view_config(context = ICourse, name = "join")
    def join(self):
        self.fikaProfile.join_course(self.context)
        return HTTPFound(location = self.request.resource_url(self.context))

    @view_config(context = ICourse, name = "leave")
    def leave(self):
        self.fikaProfile.leave_course(self.context)
        return HTTPFound(location = self.request.resource_url(self.context)) 
    

def includeme(config):
    config.scan('.courses')
