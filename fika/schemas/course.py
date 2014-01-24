import colander
import deform
from betahaus.pyracont.decorators import schema_factory


@colander.deferred
def course_module_widget(node, kw):
    view = kw['view']
    root = view.root
    values = []
    for (name, obj) in root['course_modules'].items():
        values.append((name, obj.title))
    return deform.widget.SelectWidget(values = values)


class CourseModules(colander.SequenceSchema):
    course_module = colander.SchemaNode(colander.String(),
                                        widget = course_module_widget)
    


@schema_factory('CourseSchema')
class CourseSchema(colander.Schema):
    title = colander.SchemaNode(colander.String(),)
    description = colander.SchemaNode(colander.String())
    course_modules = CourseModules()
