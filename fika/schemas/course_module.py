from arche.schemas import BaseSchema
from arche.schemas import DCMetadataSchema
from arche.interfaces import ISchemaCreatedEvent

import colander

from fika import _


class CourseModuleSchema(BaseSchema, DCMetadataSchema):
    title = colander.SchemaNode(colander.String(),
                                description = _(u"The title of the course module."))
    
def course_module_schema_adjustment(schema, event):
    if 'description' in schema:
        del schema['description']


def includeme(config):
    config.add_content_schema('CourseModule', CourseModuleSchema, 'add')
    config.add_content_schema('CourseModule', CourseModuleSchema, 'edit')
    config.add_subscriber(course_module_schema_adjustment, [CourseModuleSchema, ISchemaCreatedEvent])
