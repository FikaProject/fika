from zope.interface import implementer
from arche.api import DCMetadataMixin

from fika import FikaTSF as _
from fika.models.base import FikaBaseFolder
from fika.models.interfaces import IVideo 




@implementer(IVideo)
class Video(FikaBaseFolder, DCMetadataMixin):
    type_title = _(u"Video")
    type_name = u"Video"
    add_permission = "Add %s" % type_name
    icon = u"film"
    url = ""
    video_type= ""



def includeme(config):
    config.add_content_factory(Video)
