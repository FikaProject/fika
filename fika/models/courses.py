from betahaus.pyracont import BaseFolder
from zope.interface import implementer

from .interfaces import ICourses
from fika import FikaTSF as _


@implementer(ICourses)
class Courses(BaseFolder):
    title = display_name = _(u"Courses")
