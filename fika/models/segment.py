from zope.interface import implementer

from fika import FikaTSF as _
from fika.models.base import FikaBaseFolder
from fika.models.interfaces import ISegment                                    


@implementer(ISegment)
class Segment(FikaBaseFolder):
    type_title = _(u"Segment")
    type_name = u"Segment"
    add_permission = "Add %s" % type_name


def includeme(config):
    config.add_content_factory(Segment)
    config.add_addable_content("ImageSlideshow", "Segment")
    config.add_addable_content("Document", "Segment")
    #FIXME add video, audio, pdf here once they exist
