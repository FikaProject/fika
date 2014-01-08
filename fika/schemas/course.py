import colander
from betahaus.pyracont.decorators import schema_factory


@schema_factory('CourseSchema')
class CourseSchema(colander.Schema):
    title = colander.SchemaNode(colander.String(),)
