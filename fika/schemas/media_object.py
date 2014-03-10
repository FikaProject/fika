import colander
import deform
from betahaus.pyracont.decorators import schema_factory
from fika.schemas.youtube_node import Youtube


class MediaObject(colander.Schema):
    title = colander.SchemaNode(colander.String())
    description = colander.SchemaNode(colander.String(),
                                      missing = u"")


@schema_factory('TextMediaObjectSchema')
class TextMediaObjectSchema(MediaObject):
    body = colander.SchemaNode(colander.String(),
                               widget = deform.widget.RichTextWidget())


@schema_factory('ImageMediaObjectSchema')
class ImageMediaObjectSchema(MediaObject):
    url = colander.SchemaNode(colander.String(),)


@schema_factory('YoutubeMediaObjectSchema')
class YoutubeMediaObjectSchema(MediaObject):
    #youtube_link = colander.SchemaNode(colander.String(),)
    youtube_link = colander.SchemaNode(Youtube(),widget=deform.widget.TextInputWidget(size=60))
    
    
@schema_factory('VimeoMediaObjectSchema')
class VimeoMediaObjectSchema(MediaObject):
    vimeo_link = colander.SchemaNode(colander.String(),)
    #youtube_link = colander.SchemaNode(Youtube(),widget=deform.widget.TextInputWidget(size=60))

@schema_factory('VideoMediaObjectSchema')
class VideoMediaObjectSchema(MediaObject):
    video_link = colander.SchemaNode(colander.String(),)


@schema_factory('AudioMediaObjectSchema')
class AudioMediaObjectSchema(MediaObject):
    audio_link = colander.SchemaNode(colander.String(),)

    
    