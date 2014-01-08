from betahaus.pyracont import BaseFolder
from zope.interface import implementer

from .interfaces import IUsers
from fika import FikaTSF as _


@implementer(IUsers)
class Users(BaseFolder):
    title = display_name = _(u"Users")
