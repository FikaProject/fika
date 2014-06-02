import colander
import deform
#from betahaus.pyracont.decorators import schema_factory
from fika.schemas.youtube_node import Youtube


class MediaObject(colander.Schema):
    title = colander.SchemaNode(colander.String())
    description = colander.SchemaNode(colander.String(),
                                      validator=colander.Length(max=140),
                                      widget=deform.widget.TextAreaWidget(rows=8, cols=40),
                                      missing = u"")


class TextMediaObjectSchema(MediaObject):
    body = colander.SchemaNode(colander.String(),
                               widget = deform.widget.RichTextWidget())

class ImageMedia(colander.MappingSchema):
        url = colander.SchemaNode(colander.String(),)
        image_description = colander.SchemaNode(colander.String(),
                                      validator=colander.Length(max=1000),
                                      widget=deform.widget.TextAreaWidget(rows=8, cols=40),
                                      missing = u"")
        
class Images(colander.SequenceSchema):
    image = ImageMedia()


class ImagesMediaObjectSchema(MediaObject):
    images = Images()
    

class ImageMediaObjectSchema(MediaObject):
    url = colander.SchemaNode(colander.String(),)


class YoutubeMediaObjectSchema(MediaObject):
    #youtube_link = colander.SchemaNode(colander.String(),)
    youtube_link = colander.SchemaNode(Youtube(),widget=deform.widget.TextInputWidget(size=60))
    
    
class VimeoMediaObjectSchema(MediaObject):
    vimeo_link = colander.SchemaNode(colander.String(),)
    #youtube_link = colander.SchemaNode(Youtube(),widget=deform.widget.TextInputWidget(size=60))


class VideoMediaObjectSchema(MediaObject):
    video_link = colander.SchemaNode(colander.String(),)


class AudioMediaObjectSchema(MediaObject):
    audio_link = colander.SchemaNode(colander.String(),)

    
    