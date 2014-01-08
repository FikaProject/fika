from betahaus.pyracont import BaseFolder
from zope.interface import implementer

from .interfaces import ICourseModules


@implementer(ICourseModules)
class CourseModules(BaseFolder):
    pass
