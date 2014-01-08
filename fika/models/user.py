from repoze.folder import Folder
from zope.interface import implementer

from .interfaces import IUser


@implementer(IUser)
class User(Folder):
    pass
