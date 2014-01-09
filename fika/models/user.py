from betahaus.pyracont import BaseFolder
from betahaus.pyracont.decorators import content_factory
from zope.interface import implementer

from .interfaces import IUser
from .interfaces import IUsers


@content_factory('User')
@implementer(IUser)
class User(BaseFolder):
    allowed_contexts = (IUsers,)
    custom_fields = {'password': 'PasswordField'}
    schemas = {'add': 'UserSchema',
               'edit': 'UserSchema'}

    def default_email(self):
        try:
            return self.get_field_value('validated_emails', ())[0]
        except IndexError:
            return u''
