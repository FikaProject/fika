from zope.interface import implementer

from fika.models.base import FikaBaseFolder
from fika.models.interfaces import IImageSlideshow
from fika.schemas.course_module import CourseModuleSchema
from fika import FikaTSF as _

from arche.interfaces import IContent



@implementer(IImageSlideshow, IContent)
class ImageSlideshow(FikaBaseFolder):
    type_title = _(u"Image Slideshow")
    type_name = u"ImageSlideshow"
    title = u""
    add_permission = "Add %s" % type_name
    icon = u"picture"


def includeme(config):
    config.add_content_factory(ImageSlideshow)
    config.add_addable_content("Image", "ImageSlideshow")
