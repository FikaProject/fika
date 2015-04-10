import colander
import deform


class ImageSlideshowSchema(colander.Schema):
    title = colander.SchemaNode(colander.String(),)


def includeme(config):
    config.add_content_schema('ImageSlideshow', ImageSlideshowSchema, 'add')
    config.add_content_schema('ImageSlideshow', ImageSlideshowSchema, 'edit')
