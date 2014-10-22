from zope.interface import implementer
from arche.api import DCMetadataMixin

from fika import FikaTSF as _
from fika.models.base import FikaBaseFolder
from fika.models.interfaces import IText


@implementer(IText)
class Text(FikaBaseFolder, DCMetadataMixin):
    type_title = _(u"Text")
    type_name = u"Text"
    body = u""
    add_permission = "Add %s" % type_name
    icon = u"font"


def includeme(config):
    config.add_content_factory(Text)
