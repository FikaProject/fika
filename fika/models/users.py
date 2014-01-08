from repoze.folder import Folder
from zope.interface import implementer

from .interfaces import IUsers


@implementer(IUsers)
class Users(Folder):
    pass
