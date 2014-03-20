import colander
import deform
from betahaus.pyracont.decorators import schema_factory

@schema_factory('ModuleSegmentSchema')
class ModuleSegment(colander.Schema):
    title = colander.SchemaNode(colander.String())
    description = colander.SchemaNode(colander.String(),
                                      validator=colander.Length(max=140),
                                      widget=deform.widget.TextAreaWidget(rows=8, cols=40),
                                      missing = u"")
