from repoze.folder import Folder
from zope.interface import implementer

from .interfaces import ICourse


@implementer(ICourse)
class Course(Folder):
    pass
