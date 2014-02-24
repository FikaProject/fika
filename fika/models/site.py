from betahaus.pyracont import BaseFolder
from zope.interface import implementer

from .interfaces import ISiteRoot
from fika import security 


@implementer(ISiteRoot)
class SiteRoot(BaseFolder):
    """ Site root """
    title = u"Fika"
    __acl__ = security.DEFAULT_ACL
