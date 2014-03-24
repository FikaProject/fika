from betahaus.pyracont import BaseFolder
from zope.interface import implementer

from fika.models.interfaces import IBase


@implementer(IBase)
class FikaBaseFolder(BaseFolder):
    pass
