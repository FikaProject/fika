from betahaus.pyracont import BaseFolder
from zope.interface import implementer

from .interfaces import IUsers
from fika import FikaTSF as _


@implementer(IUsers)
class Users(BaseFolder):
    title = display_name = _(u"Users")

    def get_user_by_email(self, email):
        for obj in self.values():
            if email in obj.email:
                return obj
