from repoze.folder import Folder
from zope.interface import implementer

from .interfaces import ICourseModules


@implementer(ICourseModules)
class CourseModules(Folder):
    pass
