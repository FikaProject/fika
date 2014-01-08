from repoze.folder import Folder
from zope.interface import implementer

from .interfaces import ICourses


@implementer(ICourses)
class Courses(Folder):
    pass
