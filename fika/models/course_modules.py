from betahaus.pyracont import BaseFolder
from zope.interface import implementer

from .interfaces import ICourseModules
from fika import FikaTSF as _


@implementer(ICourseModules)
class CourseModules(BaseFolder):
    title = display_name = _(u"Course modules")
