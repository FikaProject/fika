from pyramid.security import (Authenticated,
                              NO_PERMISSION_REQUIRED,
                              ALL_PERMISSIONS,
                              DENY_ALL,
                              authenticated_userid,
                              Everyone,
                              Authenticated,
                              Allow,
                              Deny,)

from fika import FikaTSF as _


ROLE_ADMIN = u"role:Admin"
ROLE_CONTENT_MANAGER = u"role:ContentManager"

ROLES = {ROLE_ADMIN: _(u"Administrator"),
         ROLE_CONTENT_MANAGER: _(u"Content manager")}


VIEW = 'View'
EDIT = 'Edit'
DELETE = 'Delete'
MANAGE_SERVER = 'Manage server'


DEFAULT_ACL = [(Allow, ROLE_ADMIN, ALL_PERMISSIONS),
               (Allow, Authenticated, (VIEW,)),
               DENY_ALL]
