import colander
import deform
from betahaus.pyracont import BaseFolder
from betahaus.pyracont.factories import createSchema
from betahaus.pyracont.decorators import content_factory
from zope.interface import implementer

from .interfaces import IModuleSegment
from .interfaces import ICourseModule
from .interfaces import ICourse


@implementer(IModuleSegment)
class ModuleSegment(BaseFolder):
    allowed_contexts = (ICourseModule,)
    schemas = {}

    def render(self, request, view):
        schema = createSchema(self.schemas['view'])
        schema = schema.bind(context = self, request = request, view = view)
        form = deform.Form(schema, buttons = ())
        appstruct = self.get_field_appstruct(schema)
        return form.render(appstruct = appstruct, readonly = True)
        

@content_factory('TextSegment')
class TextSegment(ModuleSegment):
    schemas = {'add': 'TextSegmentSchema',
               'edit': 'TextSegmentSchema',
               'view': 'TextSegmentSchema'}
