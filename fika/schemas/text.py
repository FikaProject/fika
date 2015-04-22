import colander
import deform

from fika import _

class TextSchema(colander.Schema):
    title = colander.SchemaNode(colander.String(),
                                description=_(u"The title of the text."),)
    body = colander.SchemaNode(colander.String(),
                               widget=deform.widget.RichTextWidget(rows=24, cols=80),
                               description=_(u"Write the piece of text here."),)


def includeme(config):
    config.add_content_schema('Text', TextSchema, 'add')
    config.add_content_schema('Text', TextSchema, 'edit')
