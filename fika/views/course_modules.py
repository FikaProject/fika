from arche import security
from arche.views.base import BaseView
from pyramid.view import view_config
from pyramid.view import view_defaults

from fika import _
from fika.models.interfaces import ICourseModule
from fika.models.interfaces import ICourseModules
from fika.models.image_slideshow import ImageSlideshow
from fika.models.segment import Segment

from fika.fanstatic import lightbox_js
from fika.fanstatic import lightbox_css


@view_defaults(permission = security.PERM_VIEW)
class CourseModulesView(BaseView):

    @view_config(context = ICourseModules, renderer = "fika:templates/course_modules.pt", permission=security.PERM_VIEW)
    def course_modules(self):
        response = {}
        response['course_modules'] = self.context.values()
        response['courses'] = self.root['courses']
        response['can_create_module'] = False;
        if self.request.has_permission(security.PERM_EDIT, self.context):
            response['can_create_module'] = True;
        return response

    @view_config(context = ICourseModule, renderer = "fika:templates/course_module.pt", permission=security.PERM_VIEW)
    def course_module(self):
        response = {}
        #response['module_segments'] = self.context.values()
        response['module_segments'] = {} 
        for obj in self.context.values():
            if isinstance(obj, Segment):
                response['module_segments'][obj] = obj
                for segmentcontent in obj.values():
                    if isinstance(segmentcontent, ImageSlideshow):
                        lightbox_js.need()
                        lightbox_css.need()
                        break
        response['used_in_courses'] = self.root['courses'].module_used_in(self.context.uid)
        return response


def includeme(config):
    config.scan('.course_modules')
