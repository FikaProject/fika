import colander
from betahaus.pyracont.decorators import schema_factory


@schema_factory('CourseModuleSchema')
class CourseModuleSchema(colander.Schema):
    title = colander.SchemaNode(colander.String(),)
    description = colander.SchemaNode(colander.String(),
                                      missing = u"")
    
@schema_factory('OrderCourseModuleSchema')
class OrderCourseModuleSchema(colander.Schema):
    title = colander.SchemaNode(colander.String(),)
    
