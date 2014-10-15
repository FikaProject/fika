from arche import security
from pyramid.view import view_config
from pyramid.view import view_defaults
from pyramid.renderers import render
from pyramid.response import Response
from pyramid.traversal import find_interface

from arche.utils import get_addable_content
from arche.utils import get_content_factories

from fika import _
from fika.views.fika_base_view import FikaBaseView
from fika.views.course_pagination import render_course_pagination
from fika.models.interfaces import ICourseModule
from fika.models.interfaces import ICourse
from fika.models.image_slideshow import ImageSlideshow

from fika.fanstatic import lightbox_js
from fika.fanstatic import lightbox_css
from fika.fanstatic import common_js


@view_defaults(permission = security.PERM_VIEW)
class CourseModuleView(FikaBaseView):

    def __init__(self, context, request):
        common_js.need()
        super(CourseModuleView, self).__init__(context, request)
        self.response = {}

    @view_config(context = ICourseModule, renderer = "fika:templates/course_module.pt", permission=security.PERM_VIEW)
    def course_module(self):
        response = {}
        response['course'] = find_interface(self.context, ICourse)
        response['course_modules'] = response['course'].items()
        response['in_course'] = self.fikaProfile.in_course(response['course'])
        response['course_module_toggle'] = self._render_course_module_toggle
        response['course_pagination'] = render_course_pagination
        response['module_segments'] = {} 
        for segment in self.context.values():
            response['module_segments'][segment] = segment
            for segmentcontent in segment.values():
                if isinstance(segmentcontent, ImageSlideshow):
                    lightbox_js.need()
                    lightbox_css.need()
                    break
        response['addable_types'] = {}
        factories = get_content_factories(self.request.registry)
        for (obj, addable) in get_addable_content(self.request.registry).items():
            if 'Segment' in addable:
                factory = factories.get(obj, None)
                response['addable_types'][obj] = getattr(factory, 'icon', 'file')
        try:
            response['module_index'] = tuple(response['course'].keys()).index(self.context.__name__)+1
        except IndexError, KeyError:
            response['module_index'] = 1
        return response
    
    def _render_course_module_toggle(self, context):
        response = {'context': context,
                    'module_done': context.uid in self.fikaProfile.completed_course_modules}
        return render("fika:templates/course_module_toggle.pt", response, request = self.request)

    @view_config(name = "_set_course_module_status", context = ICourseModule)
    def course_module_status(self):
        if int(self.request.GET.get('status')):
            self.fikaProfile.completed_course_modules.add(self.context.uid)
        elif self.context.uid in self.fikaProfile.completed_course_modules:
            self.fikaProfile.completed_course_modules.remove(self.context.uid)
        return Response(self._render_course_module_toggle(self.context))


def includeme(config):
    config.scan('.course_modules')
