import colander
import deform
from betahaus.pyracont.decorators import schema_factory


@schema_factory('TextSegmentSchema')
class TextSegmentSchema(colander.Schema):
    title = colander.SchemaNode(colander.String())
    body = colander.SchemaNode(colander.String(),
                               widget = deform.widget.RichTextWidget())
