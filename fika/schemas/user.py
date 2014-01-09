import colander
from betahaus.pyracont.decorators import schema_factory

from fika import FikaTSF as _
from .common import NoDuplicates


class EmailsSchema(colander.SequenceSchema):
    email = colander.SchemaNode(colander.String(),
                                validator = colander.Email())



@schema_factory('UserSchema')
class UserSchema(colander.Schema):
    emails = EmailsSchema(validator = NoDuplicates())
    validated_emails = EmailsSchema()
