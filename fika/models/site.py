from zope.interface import implementer
from repoze.catalog.catalog import Catalog
from repoze.catalog.document import DocumentMap

from .interfaces import ISiteRoot
from .base import FikaBaseFolder
from fika import security 
from fika import FikaTSF as _
from fika.models.catalog import update_indexes


@implementer(ISiteRoot)
class SiteRoot(FikaBaseFolder):
    """ Site root """
    title =_(u"Home")
    __acl__ = security.DEFAULT_ACL

    def __init__(self, data=None, **kwargs):
        super(SiteRoot, self).__init__(data = data, **kwargs)
        self.catalog = Catalog()
        self.catalog.__parent__ = self #To make traversal work
        self.catalog.document_map = DocumentMap()
        update_indexes(self.catalog)
