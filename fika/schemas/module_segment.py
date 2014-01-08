import colander
import deform
from betahaus.pyracont.decorators import schema_factory


class ModuleSegment(colander.Schema):
    title = colander.SchemaNode(colander.String())
    description = colander.SchemaNode(colander.String())


@schema_factory('TextSegmentSchema')
class TextSegmentSchema(ModuleSegment):
    body = colander.SchemaNode(colander.String(),
                               widget = deform.widget.RichTextWidget())
