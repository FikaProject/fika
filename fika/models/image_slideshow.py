from zope.interface import implementer
from arche.api import DCMetadataMixin

from fika import FikaTSF as _
from fika.models.base import FikaBaseFolder
from fika.models.interfaces import IImageSlideshow




@implementer(IImageSlideshow)
class ImageSlideshow(FikaBaseFolder, DCMetadataMixin):
    type_title = _(u"Image Slideshow")
    type_name = u"ImageSlideshow"
    add_permission = "Add %s" % type_name
    icon = u"picture"
    
    @property
    def title(self):
        return self.uid


def includeme(config):
    config.add_content_factory(ImageSlideshow)
    config.add_addable_content("Image", "ImageSlideshow")
