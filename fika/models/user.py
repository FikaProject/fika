from betahaus.pyracont import BaseFolder
from betahaus.pyracont.decorators import content_factory
from zope.interface import implementer

from .interfaces import IUser
from .interfaces import IUsers


@content_factory('User')
@implementer(IUser)
class User(BaseFolder):
    allowed_contexts = (IUsers,)
    schemas = {'add': 'UserSchema',
               'edit': 'UserSchema'}
