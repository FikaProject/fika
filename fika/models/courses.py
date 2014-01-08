from betahaus.pyracont import BaseFolder
from zope.interface import implementer

from .interfaces import ICourses


@implementer(ICourses)
class Courses(BaseFolder):
    pass
