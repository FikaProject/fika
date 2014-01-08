from repoze.folder import Folder
from zope.interface import implementer

from .interfaces import IModuleSegment


@implementer(IModuleSegment)
class ModuleSegment(Folder):
    pass
