from pyramid.view import view_config
from pyramid.view import view_defaults
from pyramid.renderers import render
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound
#from betahaus.pyracont.interfaces import IBaseFolder
from arche.views.base import BaseView
from arche import security

#from fika.views.base import BaseView
from fika.models.interfaces import ICourse
from fika.models.interfaces import ICourseModule
from fika.models.interfaces import ICourses
from fika.models.interfaces import IFikaUser
#from fika import security
from fika.fanstatic import main_css
from fika.fanstatic import common_js

@view_defaults(permission = security.PERM_VIEW)
class CourseView(BaseView):

    @property
    def profile(self):
        if self.request.authenticated_userid:
            user = self.root['users'][self.request.authenticated_userid]
            return self.request.registry.getAdapter(user, IFikaUser)

    def __init__(self, context, request):
        main_css.need()
        common_js.need()
        super(CourseView, self).__init__(context, request)
        self.response = {}

    @view_config(context = ICourse, renderer = "fika:templates/course.pt")
    def course(self):
        pages = self.context.cm_pages()

        def _next(page):
            next = page + 1
            return page < len(pages) - 1 and "?p=%s" % next or ""

        def _previous(page):
            previos = page - 1
            return page > 0 and "?p=%s" % previos or ""
            
        #course_modules = self.root['course_modules']
        course_modules = {}
        for uid in self.context.course_modules:
            course_modules[uid] = self.resolve_uid(uid)
        page = int(self.request.GET.get('p', 0))
        self.response['page'] = page
        self.response['pages'] = pages
        cm_uid = pages.get(page)
        self.response['course_module'] = course_modules.get(cm_uid, None)
        self.response['next'] = _next
        self.response['previous'] = _previous
        self.response['course_modules'] = course_modules
        self.response['in_course'] = self.profile.in_course(self.context)
        self.response['course_module_toggle'] = self._render_course_module_toggle
        return self.response

    def _render_course_module_toggle(self, context):
        response = {'context': context,
                    'module_done': context.uid in self.profile.completed_course_modules}
        return render("fika:templates/course_module_toggle.pt", response, request = self.request)

    @view_config(name = "_set_course_module_status", context = ICourseModule)
    def course_module_status(self):
        if int(self.request.GET.get('status')):
            self.profile.completed_course_modules.add(self.context.uid)
        elif self.context.uid in self.profile.completed_course_modules:
            self.profile.completed_course_modules.remove(self.context.uid)
        return Response(self._render_course_module_toggle(self.context))

    @view_config(context = ICourses, renderer = "fika:templates/courses.pt")
    def courses(self):
        self.response['courses'] = self.context.values()
        self.response['course_modules'] = self.root['course_modules']
        return self.response
    
    @view_config(context = ICourse, name = "join")
    def join(self):
        self.profile.join_course(self.context)
        return HTTPFound(location = self.request.resource_url(self.context))

    @view_config(context = ICourse, name = "leave")
    def leave(self):
        self.profile.leave_course(self.context)
        return HTTPFound(location = self.request.resource_url(self.context)) 

def includeme(config):
    config.scan('.courses')
