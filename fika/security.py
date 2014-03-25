from pyramid.security import (Authenticated,
                              NO_PERMISSION_REQUIRED,
                              ALL_PERMISSIONS,
                              DENY_ALL,
                              authenticated_userid,
                              Everyone,
                              Authenticated,
                              Allow,
                              Deny,)
from pyramid.interfaces import IAuthorizationPolicy
from pyramid.threadlocal import get_current_registry
from pyramid.threadlocal import get_current_request

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

def context_has_permission(context, permission, userid = None):
    """ Special permission check that is agnostic of the request.context attribute.
        (As opposed to pyramid.security.has_permission)
        Don't use anything else than this one to determine permissions for something
        where the request.context isn't the same as context, for instance another 
        object that appears in a listing.
    """
    request = get_current_request()
    if userid is None:
        userid = authenticated_userid(request)
    principals = context_effective_principals(context, userid)
    authz_policy = request.registry.getUtility(IAuthorizationPolicy)
    return authz_policy.permits(context, principals, permission)

def context_effective_principals(context, userid):
    """ Special version of pyramid.security.effective_principals that
        adds groups based on context instead of request.context
        
        A note about Authenticated: It doesn't mean that the current user is authenticated,
        rather than someone with a userid are part of the Authenticated group, since by using
        a userid they will have logged in :)
    """
    effective_principals = [Everyone]
    if userid is None:
        return effective_principals
    sec = get_security(context)
    groups = sec.get_groups(userid)
    effective_principals.append(Authenticated)
    effective_principals.append(userid)
    effective_principals.extend(groups)
    return effective_principals
