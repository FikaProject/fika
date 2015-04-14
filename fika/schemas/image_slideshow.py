import colander
import deform

from arche.schemas import AddFileSchema
from arche.interfaces import ISchemaCreatedEvent


class ImageSlideshowSchema(colander.Schema):
    title = colander.SchemaNode(colander.String(),)
    
class AddImageSchema(AddFileSchema):
    pass

def image_schema_adjustment(schema, event):
    if 'title' in schema:
        del schema['title']


def includeme(config):
    config.add_content_schema('ImageSlideshow', ImageSlideshowSchema, 'add')
    config.add_content_schema('ImageSlideshow', ImageSlideshowSchema, 'edit')
    config.add_content_schema('Image', AddImageSchema, 'add') #Specific schema?
    config.add_content_schema('Image', AddImageSchema, 'edit')
    config.add_subscriber(image_schema_adjustment, [AddImageSchema, ISchemaCreatedEvent])
