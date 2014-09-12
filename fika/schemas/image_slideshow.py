import colander
import deform


class ImageSlideshowSchema(colander.Schema):
    title = colander.SchemaNode(colander.String(),)
    description = colander.SchemaNode(colander.String(),
                                      validator=colander.Length(max=140),
                                      widget=deform.widget.TextAreaWidget(rows=8, cols=40),
                                      missing = u"")


def includeme(config):
    config.add_content_schema('ImageSlideshow', ImageSlideshowSchema, 'add')
    config.add_content_schema('ImageSlideshow', ImageSlideshowSchema, 'edit')