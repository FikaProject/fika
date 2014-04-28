import colander
import deform


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


class CourseSchema(colander.Schema):
    title = colander.SchemaNode(colander.String(),)
    description = colander.SchemaNode(colander.String(),
                                      validator=colander.Length(max=1000),
                                      widget=deform.widget.TextAreaWidget(rows=8, cols=40),
                                      missing = u"")
    introduction = colander.SchemaNode(colander.String(),
                               widget = deform.widget.RichTextWidget(),
                               missing = u"")
    course_modules = CourseModules(widget=deform.widget.SequenceWidget(orderable=True))


def includeme(config):
    config.add_content_schema('Course', CourseSchema, 'add')
    config.add_content_schema('Course', CourseSchema, 'edit')
