from pyramid.view import view_config
from pyramid.view import view_defaults
from pyramid.renderers import render
from pyramid.security import Allowed
from pyramid.traversal import resource_path
from pyramid.httpexceptions import HTTPFound

from arche import security
from arche.utils import get_addable_content
from arche.utils import get_content_factories

from fika.views.fika_base_view import FikaBaseView
from fika.models.interfaces import ICourse
from fika.models.interfaces import ICourseModule
from fika.models.interfaces import ICourses
from fika.views.course_pagination import render_course_pagination

@view_defaults(permission = security.PERM_VIEW)
class CourseView(FikaBaseView):

    @view_config(context = ICourse, renderer = "fika:templates/course.pt", permission=security.PERM_VIEW)
    def course(self):
        response = {}
        response['course_modules'] = self.context.values()
        response['in_course'] = self.fikaProfile.in_course(self.context)
        response['course_pagination'] = render_course_pagination
        
        response['course_modules_media'] = {}
        for course_module in response['course_modules']:
            response['course_modules_media'][course_module.uid] = {}
            for segment in course_module.values():
                for media in segment.values():
                    if not hasattr(media, 'icon'):
                        continue
                    if media.icon in response['course_modules_media'][course_module.uid]:
                        response['course_modules_media'][course_module.uid][media.icon] += 1
                    else:
                        response['course_modules_media'][course_module.uid][media.icon] = 1
        return response
    
    @view_config(context = ICourses, renderer = "fika:templates/courses.pt", permission=security.PERM_VIEW)
    def courses(self):
        response = {}
        response['courses'] = [x for x in self.context.values() if self.request.has_permission(security.PERM_VIEW, x)]
        response['can_create_course'] = False;
        if self.request.has_permission(security.PERM_EDIT, self.context):
            response['can_create_course'] = True;
        response['num_modules'] = {}
        response['num_media'] = {}
        for course in response['courses']:
            response['num_modules'][course] = len(self.catalog_search(resolve = False,
                                                                      path = resource_path(course),
                                                                      type_name='CourseModule'))
            response['num_media'][course] = {}
            addable_types = {}
            factories = get_content_factories(self.request.registry)
            for (obj, addable) in get_addable_content(self.request.registry).items():
                if 'Segment' in addable:
                    factory = factories.get(obj, None)
                    addable_types[obj] = getattr(factory, 'icon', 'file')
            for (media, icon) in addable_types.items():
                response['num_media'][course][icon] = len(self.catalog_search(resolve = False,
                                                                             path = resource_path(course),
                                                                             type_name=media))
        return response
    
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
