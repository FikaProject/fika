import colander
from arche import _
from arche import security
from arche.fanstatic_lib import jqueryui
from arche.fanstatic_lib import touchpunch_js
from arche.utils import get_addable_content
from arche.utils import get_content_factories
from arche.utils import get_content_views
from arche.schemas import BaseSchema
from arche.widgets import ReferenceWidget
from arche.views.base import DefaultEditForm, BaseForm
from arche.utils import send_email
from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPNotFound
from pyramid.traversal import resource_path
from pyramid.view import view_config
from pyramid.view import view_defaults
from pyramid_deform import FormView

from betahaus.viewcomponent import view_action

from fika.models.interfaces import ICourse
from fika.models.interfaces import ICourses
from fika.models.interfaces import IFikaUser
from fika.views.course_pagination import render_course_pagination
from fika.views.fika_base_view import FikaBaseView
from fika.models.interfaces import IAssessment


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
    
    
    
    @view_config(context = ICourse, name = "responses_overview", renderer = "fika:templates/responses_overview.pt", permission=security.PERM_EDIT)
    def responses_overview(self):
        response = {}
        response['answers'] = {}
        response['user_answers'] = {}
        for module in self.context.values():
            for segment in module.values():
                if IAssessment.providedBy(segment):
                    response['answers'][segment.uid] = {}
                    for answer in segment.values():
                        response['answers'][segment.uid][answer.uid] = answer
                        if answer.user_uid not in response['user_answers']:
                            response['user_answers'][answer.user_uid] = {}
                        response['user_answers'][answer.user_uid][segment.uid] = answer.uid
                        
        return response
    
@view_action('actions_menu', 'responses_overview',
             title = _("Responses overview"),
             permission = security.PERM_EDIT, #FIXME which permission do you need here?
             priority = 50)
def actionbar_responses_overview(context, request, va, **kw):
    if ICourse.providedBy(context):
        return """<li><a href="%(url)s">%(title)s</a></li>""" %\
            {'url': request.resource_url(context, 'responses_overview'),
             'title': va.title}
                    
                    
        

@view_action('actions_menu', 'assign_course',
             title = _("Assign to user"),
             permission = security.PERM_EDIT, #FIXME which permission do you need here?
             priority = 60)
def actionbar_assign(context, request, va, **kw):
    if ICourse.providedBy(context):
        return """<li><a href="%(url)s">%(title)s</a></li>""" %\
            {'url': request.resource_url(context, 'assign_course'),
             'title': va.title}


class AssignCourseSchema(BaseSchema):
    users = colander.SchemaNode(colander.List(),
                                   title = _(u"Select content to show"),
                                   missing = colander.null,
                                   widget = ReferenceWidget(query_params = {'type_name': 'User'}))

#@view_config(context = ICourse, name = "assign_course", renderer = "fika:templates/assign_course.pt")
class AssignCourseForm(BaseForm):
    type_name = u'Course'
    schema_name = 'assign_course'
    title = _(u"Assign course to users")

    def __call__(self):
        contents = []
        #import pdb;pdb.set_trace()
        for name in self.root['users']:
            user = self.root['users'][name]
            if self.context.__name__ in user.__courses__:
                contents.append(name)
        #return {'contents': contents}
        result = super(AssignCourseForm, self).__call__()
        return result
    
    def save_success(self, appstruct):
        nr_of_users = 0
        if not appstruct['users']:
            return HTTPFound(location = self.request.resource_url(self.context))
        for uid in appstruct['users']:
                user = self.resolve_uid(uid)
                fikauser = IFikaUser(self.resolve_uid(uid), None)
                if fikauser is not None:
                    fikauser.join_course(self.context)
                    email_html = '<h4>Hello '+user.first_name+' '+user.last_name+ \
                                ',</h4><p>You have been assigned to the course \"'+self.context.title+ \
                                '\" by '+self.profile.first_name + ' ' + self.profile.last_name+'. You will now see it in the \'My Courses\' list when you log in to '+self.root.title+'.'
                    send_email('You have been assigned a course', user.email, email_html, send_immediately=True)
                    nr_of_users += 1
        plural = "s" if nr_of_users != 1 else ""
        self.flash_messages.add(_(u"Assigned course to "+str(nr_of_users)+" user"+plural+"."), type="success")
        return HTTPFound(location = self.request.resource_url(self.context))
    
    

def includeme(config):
    config.add_content_schema('Course', AssignCourseSchema, 'assign_course')
    config.add_view(AssignCourseForm,
                context = ICourse,
                name = 'assign_course',
                permission = security.PERM_EDIT,
                renderer = 'arche:templates/form.pt')