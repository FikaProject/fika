from arche.schemas import BaseSchema
from arche.schemas import DCMetadataSchema
from arche.widgets import FileAttachmentWidget
import colander
import deform

from fika import _


class CourseSchema(DCMetadataSchema, BaseSchema):
    title = colander.SchemaNode(colander.String(),
                                description = u"The title of the course.")
    description = colander.SchemaNode(colander.String(),
                                      description = u"A short description of the course.",
                                      validator=colander.Length(max=1000),
                                      widget=deform.widget.TextAreaWidget(rows=8, cols=40),
                                      missing = u"")
    introduction = colander.SchemaNode(colander.String(),
                               description=u"Describe who the course is for, why the course is relevant, and give a short example of a problem the course will help in solving.",
                               widget = deform.widget.RichTextWidget(),
                               missing = u"")
    image_data = colander.SchemaNode(deform.FileData(),
                                     description=u"(Optional) An image that will be shown next to the description.",
                                     missing = None,
                                     title = _(u"Image"),
                                     widget = FileAttachmentWidget())


def includeme(config):
    config.add_content_schema('Course', CourseSchema, 'add')
    config.add_content_schema('Course', CourseSchema, 'edit')
