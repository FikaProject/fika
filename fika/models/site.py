from betahaus.pyracont import BaseFolder
from zope.interface import implementer

from .interfaces import ISiteRoot


@implementer(ISiteRoot)
class SiteRoot(BaseFolder):
    """ Site root """
    title = u"Fika"

