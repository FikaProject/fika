from betahaus.pyracont.decorators import content_factory
from zope.interface import implementer

from .interfaces import ICourse
from .interfaces import ICourses
from .base import FikaBaseFolder


@content_factory('Course')
@implementer(ICourse)
class Course(FikaBaseFolder):
    allowed_contexts = (ICourses,)
    schemas = {'add': 'CourseSchema',
               'edit': 'CourseSchema',
               'delete': 'DeleteSchema'}
