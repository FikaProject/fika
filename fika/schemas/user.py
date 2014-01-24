import colander
import deform
from betahaus.pyracont.decorators import schema_factory

from fika import FikaTSF as _
from .common import NoDuplicates


class EmailsSchema(colander.SequenceSchema):
    email = colander.SchemaNode(colander.String(),
                                validator = colander.Email())


    
@colander.deferred
def course_widget(node, kw):
    view = kw['view']
    root = view.root
    values = []
    for (name, obj) in root['courses'].items():
        values.append((name, obj.title))
    return deform.widget.SelectWidget(values = values)

class CoursesSchema(colander.SequenceSchema):
    course = colander.SchemaNode(colander.String(), widget = course_widget)


@schema_factory('UserSchema')
class UserSchema(colander.Schema):
    emails = EmailsSchema(validator = NoDuplicates())
    validated_emails = EmailsSchema()
    courses = CoursesSchema(validator = NoDuplicates())
    


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
