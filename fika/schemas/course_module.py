from arche.schemas import BaseSchema
from arche.schemas import DCMetadataSchema
import colander
import deform


class CourseModuleSchema(BaseSchema, DCMetadataSchema):
    title = colander.SchemaNode(colander.String(),
                                description = u"The title of the course module.")
    description = colander.SchemaNode(colander.String(),
                                      description = u"A short description of the course module.",
                                      validator=colander.Length(max=140),
                                      widget=deform.widget.TextAreaWidget(rows=8, cols=40),
                                      missing = u"")


def includeme(config):
    config.add_content_schema('CourseModule', CourseModuleSchema, 'add')
    config.add_content_schema('CourseModule', CourseModuleSchema, 'edit')
