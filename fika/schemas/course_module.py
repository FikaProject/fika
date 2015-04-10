from arche.schemas import BaseSchema
from arche.schemas import DCMetadataSchema
import colander
import deform


class CourseModuleSchema(BaseSchema, DCMetadataSchema):
    title = colander.SchemaNode(colander.String(),
                                description = u"The title of the course module.")


def includeme(config):
    config.add_content_schema('CourseModule', CourseModuleSchema, 'add')
    config.add_content_schema('CourseModule', CourseModuleSchema, 'edit')
