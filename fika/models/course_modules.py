from zope.interface import implementer

from .interfaces import ICourseModules
from .base import FikaBaseFolder
from fika import FikaTSF as _


@implementer(ICourseModules)
class CourseModules(FikaBaseFolder):
    title = display_name = _(u"Course modules")
