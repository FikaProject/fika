import colander
import deform
from betahaus.pyracont.decorators import schema_factory


@schema_factory('CourseModuleSchema')
class CourseModuleSchema(colander.Schema):
    title = colander.SchemaNode(colander.String(),)
    description = colander.SchemaNode(colander.String(),
                                      validator=colander.Length(max=140),
                                      widget=deform.widget.TextAreaWidget(rows=8, cols=40),
                                      missing = u"")
    

class Segment(colander.Schema):
            segment = colander.SchemaNode(colander.String())
            
class Segments(colander.SequenceSchema):
            segment = Segment()

@schema_factory('OrderCourseModuleSchema')
class OrderCourseModuleSchema(colander.Schema):
    segments = Segments(
                widget=deform.widget.SequenceWidget(orderable=True)
            )
    