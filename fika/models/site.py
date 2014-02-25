from zope.interface import implementer

from .interfaces import ISiteRoot
from .base import FikaBaseFolder
from fika import security 
from fika import FikaTSF as _

@implementer(ISiteRoot)
class SiteRoot(FikaBaseFolder):
    """ Site root """
    title =_(u"Home")
    __acl__ = security.DEFAULT_ACL
