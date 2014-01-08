from betahaus.pyracont import BaseFolder
from zope.interface import implementer

from .interfaces import IModuleSegment


@implementer(IModuleSegment)
class ModuleSegment(BaseFolder):
    pass
