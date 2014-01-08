from betahaus.pyracont import BaseFolder
from betahaus.pyracont.decorators import content_factory
from zope.interface import implementer

from .interfaces import ICourseModule
from .interfaces import ICourseModules


@content_factory('CourseModule')
@implementer(ICourseModule)
class CourseModule(BaseFolder):
    allowed_contexts = (ICourseModules,)
