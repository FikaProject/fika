from repoze.folder import Folder
from zope.interface import implementer

from .interfaces import ICourseModule


@implementer(ICourseModule)
class CourseModule(Folder):
    pass
