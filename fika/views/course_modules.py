import colander
import deform

from js.deform import auto_need
from js.jqueryui import jqueryui

from pyramid.view import view_config
from pyramid.view import view_defaults
from pyramid.httpexceptions import HTTPFound

from betahaus.pyracont.factories import createSchema

from fika import security
from fika.views.base import BaseView
from fika.models.interfaces import ICourseModule
from fika.models.interfaces import ICourseModules
from fika.models.interfaces import IModuleSegment
from fika.models.media_object import YoutubeMediaObject, ImageMediaObject

@view_defaults(permission = security.VIEW)
class CourseModulesView(BaseView):

    @view_config(context = ICourseModules, renderer = "fika:templates/course_modules.pt")
    def course_modules(self):
        self.response['course_modules'] = self.context.values()
        self.response['courses'] = self.root['courses']
        return self.response

    @view_config(context = ICourseModule, renderer = "fika:templates/course_module.pt")
    def course_module(self):
        self.response['module_segments'] = self.context.values()
        self.response['used_in_courses'] = self.root['courses'].module_used_in(self.context.uid)
        return self.response
    
    @view_config(context = ICourseModule, name = "edit", renderer = "fika:templates/course_module.pt")
    def edit(self):
        jqueryui.need()
        schema = createSchema(self.context.schemas['edit'])
        schema = schema.bind(context = self.context, request = self.request, view = self)
        form = deform.Form(schema, buttons = ('save', 'cancel'), action="#")
        auto_need(form)
        if self.request.method == 'POST':
            if 'save' in self.request.POST:
                controls = self.request.POST.items()
                try:
                    appstruct = form.validate(controls)
                except deform.ValidationFailure, e:
                    self.response['form'] = e.render()
                    self.response['module_segments'] = self.context.values()
                    self.response['used_in_courses'] = self.root['courses'].module_used_in(self.context.uid)
                    return self.response
                self.context.set_field_appstruct(appstruct)
            return HTTPFound(location = self.request.resource_url(self.context))
        appstruct = self.context.get_field_appstruct(schema)
        self.response['form'] = form.render(appstruct = appstruct)
        self.response['module_segments'] = self.context.values()
        self.response['used_in_courses'] = self.root['courses'].module_used_in(self.context.uid)
        return self.response
    
    @view_config(context = ICourseModule, name = 'order', permission = security.EDIT, renderer = "fika:templates/course_module.pt")
    def ordering(self):
        #FIXME not done! This view needs to write the keys within this context to context.order
        self.response['module_segments'] = self.context.values()
        self.response['used_in_courses'] = self.root['courses'].module_used_in(self.context.uid)
        #import pdb;pdb.set_trace()
        schema = createSchema(self.context.schemas['order'])
        schema = schema.bind(context = self.context, request = self.request, view = self)
        form = deform.Form(schema, buttons = ('save', 'cancel'), action="#")
        appstruct = self.context.get_field_appstruct(schema)
        self.response['form'] = form.render(appstruct = appstruct)
        return self.response
