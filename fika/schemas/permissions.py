import colander
import deform
from betahaus.pyracont.decorators import schema_factory

from fika import security
from fika import FikaTSF as _


@colander.deferred
def deferred_roles_widget(node, kw):
    """ Only handles role-like groups with prefix 'role:'"""
    return deform.widget.CheckboxChoiceWidget(values=security.ROLES.items(),
                                              missing=colander.null,)


class UserIDAndGroupsSchema(colander.Schema):
    userid = colander.SchemaNode(
        colander.String(),
        title = _(u"UserID"),
    )
    #It's called groups here, but we restrict choices to roles only
    groups = colander.SchemaNode(
        deform.Set(allow_empty=True),
        title = _(u"Groups"),
        widget = deferred_roles_widget,
        #validator = deferred_context_roles_validator,
    )


class UserIDsAndGroupsSequenceSchema(colander.SequenceSchema):
    userid_and_groups = UserIDAndGroupsSchema(title=_(u'Roles for user'),)


@schema_factory('PermissionsSchema',
                title = _(u"Permissions"),
                description = _(u"permissions_schema_main_description",
                                default = u"Set permission for each UserID that should have rights in this meeting. If you remove a UserID, their permissions will be cleared."))
class PermissionsSchema(colander.Schema):
    userids_and_groups = UserIDsAndGroupsSequenceSchema(title=_(u'Role settings for users'))
