from betahaus.pyracont import BaseFolder
from zope.interface import implementer

from .interfaces import IUser


@implementer(IUser)
class User(BaseFolder):
    pass
