from betahaus.pyracont import BaseFolder
from zope.interface import implementer

from .interfaces import ICourseModule


@implementer(ICourseModule)
class CourseModule(BaseFolder):
    pass
