from betahaus.pyracont import BaseFolder
from betahaus.pyracont.decorators import content_factory
from zope.interface import implementer

from .interfaces import ICourse
from .interfaces import ICourses


@content_factory('Course')
@implementer(ICourse)
class Course(BaseFolder):
    allowed_contexts = (ICourses,)
