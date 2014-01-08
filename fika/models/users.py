from betahaus.pyracont import BaseFolder
from zope.interface import implementer

from .interfaces import IUsers


@implementer(IUsers)
class Users(BaseFolder):
    pass
