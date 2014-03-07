import colander
import deform
from betahaus.pyracont.decorators import schema_factory

@schema_factory('ModuleSegmentSchema')
class ModuleSegment(colander.Schema):
    title = colander.SchemaNode(colander.String())
    description = colander.SchemaNode(colander.String(),
                                      missing = u"")
