from betahaus.pyracont.decorators import content_factory
from zope.interface import implementer

from .base import FikaBaseFolder
from .interfaces import ICourseModule
from .interfaces import ICourseModules


@content_factory('CourseModule')
@implementer(ICourseModule)
class CourseModule(FikaBaseFolder):
    allowed_contexts = (ICourseModules,)
    schemas = {'add': 'CourseModuleSchema',
               'edit': 'CourseModuleSchema',
               'delete': 'DeleteSchema'}
    custom_accessors = {'order':'get_order'}
    custom_mutators = {'order':'set_order'}

    def get_order(self, **kwargs):
        return tuple(self.order)
    
    def set_order(self, value, **kwargs):
        self.order = value
