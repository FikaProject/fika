from repoze.folder import Folder
from zope.interface import implementer

from .interfaces import ISiteRoot


@implementer(ISiteRoot)
class SiteRoot(Folder):
    """ Site root """
    title = u"Fika"

