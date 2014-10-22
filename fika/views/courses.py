from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.view import view_config
from pyramid.view import view_defaults
from pyramid.renderers import render
from pyramid.security import Allowed
from pyramid.traversal import resource_path

from arche import security
from arche.utils import get_addable_content
from arche.utils import get_content_factories
from arche.fanstatic_lib import jqueryui, touchpunch_js

from fika.views.fika_base_view import FikaBaseView
from fika.models.interfaces import ICourse
from fika.models.interfaces import ICourseModule
from fika.models.interfaces import ICourses
from fika.views.course_pagination import render_course_pagination

@view_defaults(permission = security.PERM_VIEW)
class CourseView(FikaBaseView):
    
    def __call__(self):
        content_keys = self.request.POST.getall('content_name')
        keys = set(self.context.keys())
        for item in content_keys:
            if item not in keys:
                return HTTPNotFound()
            keys.remove(item)
        content_keys.extend(keys)
        self.context.order = content_keys
        return HTTPFound(location = self.request.resource_url(self.context))

    @view_config(context = ICourse, renderer = "fika:templates/course.pt", permission=security.PERM_VIEW)
    def course(self):
        if self.request.has_permission('perm:Edit', self.context):
            jqueryui.need()
            touchpunch_js.need()
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
        response['can_create_course'] = False;
        if self.request.has_permission(security.PERM_EDIT, self.context):
            response['can_create_course'] = True;
        addable_types = {}
        factories = get_content_factories(self.request.registry)
        for (obj, addable) in get_addable_content(self.request.registry).items():
            if 'Segment' in addable:
                factory = factories.get(obj, None)
                addable_types[obj] = getattr(factory, 'icon', 'file')
        response['courses'] = courses = []
        response['num_modules'] = {}
        response['num_media'] = {}
        for (name, course) in self.context.items():
            if not self.request.has_permission(security.PERM_VIEW, course):
                continue
            courses.append(course)
            response['num_modules'][name] = len(self.catalog_search(resolve = False,
                                                                    path = resource_path(course),
                                                                    type_name='CourseModule'))
            response['num_media'][name] = {}
            for (media, icon) in addable_types.items():
                response['num_media'][name][icon] = len(self.catalog_search(resolve = False,
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
    
    @view_config(context = ICourse, name = "sorted")
    def sorted(self):
        module_names = self.request.POST.getall('module_name')
        keys = set(self.context.keys())
        for item in module_names:
            if item not in keys:
                return HTTPNotFound()
            keys.remove(item)
        module_names.extend(keys)
        self.context.order = module_names
        return HTTPFound(location = self.request.resource_url(self.context))
    

def includeme(config):
    config.scan('.courses')
