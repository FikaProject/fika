from pyramid.security import (Authenticated,
                              NO_PERMISSION_REQUIRED,
                              ALL_PERMISSIONS,
                              DENY_ALL,
                              authenticated_userid,
                              Everyone,
                              Authenticated,
                              Allow,
                              Deny,)
from pyramid.threadlocal import get_current_registry

from fika import FikaTSF as _
from fika.models.interfaces import ISecurity


ROLE_ADMIN = u"role:Admin"
ROLE_CONTENT_MANAGER = u"role:ContentManager"
ROLE_OWNER = u"role:Owner"

ROLES = {ROLE_ADMIN: _(u"Administrator"),
         ROLE_CONTENT_MANAGER: _(u"Content manager")}


VIEW = 'View'
EDIT = 'Edit'
DELETE = 'Delete'
MANAGE_SERVER = 'Manage server'


DEFAULT_ACL = [(Allow, ROLE_ADMIN, ALL_PERMISSIONS),
               (Allow, Authenticated, (VIEW,)),
               (Allow, ROLE_OWNER, EDIT),
               DENY_ALL]


def get_security(context, reg = None):
    if reg is None:
        reg = get_current_registry()
    return reg.getAdapter(context, ISecurity)
