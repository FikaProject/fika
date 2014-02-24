from zope.interface import implementer

from .interfaces import ISiteRoot
from .base import FikaBaseFolder
from fika import security 


@implementer(ISiteRoot)
class SiteRoot(FikaBaseFolder):
    """ Site root """
    title = u"Fika"
    __acl__ = security.DEFAULT_ACL
