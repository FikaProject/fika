import colander
import deform
from betahaus.pyracont.decorators import schema_factory
from fika.schemas.youtube_node import Youtube


class ModuleSegment(colander.Schema):
    title = colander.SchemaNode(colander.String())
    description = colander.SchemaNode(colander.String())
    order = colander.SchemaNode(colander.String(),)


@schema_factory('TextSegmentSchema')
class TextSegmentSchema(ModuleSegment):
    body = colander.SchemaNode(colander.String(),
                               widget = deform.widget.RichTextWidget())
    
@schema_factory('ImageSegmentSchema')
class ImageSegmentSchema(ModuleSegment):
    url = colander.SchemaNode(colander.String(),)

@schema_factory('YoutubeSegmentSchema')
class YoutubeSegmentSchema(ModuleSegment):
    #youtube_link = colander.SchemaNode(colander.String(),)
    youtube_link = colander.SchemaNode(Youtube(),widget=deform.widget.TextInputWidget(size=60))
    