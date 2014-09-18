from zope.interface import implementer

from fika.models.base import FikaBaseFolder
from fika.models.interfaces import ISegment                                    
from fika import FikaTSF as _

from arche.interfaces import (IContent,
                              IDocument)


@implementer(ISegment, IContent)
class Segment(FikaBaseFolder):
    type_title = _(u"Segment")
    type_name = u"Segment"
    title = u""
    add_permission = "Add %s" % type_name


def includeme(config):
    config.add_content_factory(Segment)
    config.add_addable_content("ImageSlideshow", "Segment")
    config.add_addable_content("Document", "Segment")
    config.add_addable_content("ExternalResource", "Segment")
    #FIXME add video, audio, pdf here once they exist
