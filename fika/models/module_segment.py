import colander
import deform
from betahaus.pyracont.factories import createSchema
from betahaus.pyracont.decorators import content_factory
from zope.interface import implementer

from .base import FikaBaseFolder
from .interfaces import IModuleSegment
from .interfaces import ICourseModule
from .interfaces import ICourse

@content_factory('ModuleSegment')
@implementer(IModuleSegment)
class ModuleSegment(FikaBaseFolder):
    allowed_contexts = (ICourseModule,)
    schemas = {'add': 'ModuleSegmentSchema',
               'edit': 'ModuleSegmentSchema',
               'delete': 'DeleteSchema'}
