from arche.schemas import file_upload_widget
import colander
import deform

from fika import _


class CourseSchema(colander.Schema):
    title = colander.SchemaNode(colander.String(),)
    description = colander.SchemaNode(colander.String(),
                                      validator=colander.Length(max=1000),
                                      widget=deform.widget.TextAreaWidget(rows=8, cols=40),
                                      missing = u"")
    introduction = colander.SchemaNode(colander.String(),
                               widget = deform.widget.RichTextWidget(),
                               missing = u"")
    image_data = colander.SchemaNode(deform.FileData(),
                                     missing = None,
                                     title = _(u"Image"),
                                     widget = file_upload_widget)


def includeme(config):
    config.add_content_schema('Course', CourseSchema, 'add')
    config.add_content_schema('Course', CourseSchema, 'edit')
