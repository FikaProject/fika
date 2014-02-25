import colander
import deform
from betahaus.pyracont.decorators import schema_factory

from fika import FikaTSF as _
from .common import NoDuplicates


@schema_factory('UserSchema')
class UserSchema(colander.Schema):
    name = colander.SchemaNode(colander.String(),
                               title = _(u"Your name"),
                               missing = u"")
    email = colander.SchemaNode(colander.String(),
                                validator = colander.Email())


@schema_factory('RegisterUserSchema')
class RegisterUserSchema(colander.Schema):
    email = colander.SchemaNode(colander.String(),
                                validator = colander.Email())
    password = colander.SchemaNode(colander.String(),
                                   widget = deform.widget.CheckedPasswordWidget(size=20),
                                   validator = colander.Length(min = 6, max = 100))


@schema_factory('ChangeUserPasswordSchema')
class ChangeUserPasswordSchema(colander.Schema):
    password = colander.SchemaNode(colander.String(),
                                   widget = deform.widget.CheckedPasswordWidget(size=20),
                                   validator = colander.Length(min = 6, max = 100))


@schema_factory('LoginSchema')
class LoginSchema(colander.Schema):
    email = colander.SchemaNode(colander.String(),
                                validator = colander.Email())
    password = colander.SchemaNode(colander.String(),
                                   widget = deform.widget.PasswordWidget())
