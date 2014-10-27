import colander
import deform


class TextSchema(colander.Schema):
    title = colander.SchemaNode(colander.String(),
                                description=u"The title of the text.",)
    description = colander.SchemaNode(colander.String(),
                                      validator=colander.Length(max=140),
                                      widget=deform.widget.TextAreaWidget(rows=8, cols=40),
                                      missing = u"",
                                      description=u"Write a short description of the text here. Max 140 characters.",)
    body = colander.SchemaNode(colander.String(),
                               widget=deform.widget.RichTextWidget(rows=8, cols=80),
                               description=u"Write the piece of text here.",)


def includeme(config):
    config.add_content_schema('Text', TextSchema, 'add')
    config.add_content_schema('Text', TextSchema, 'edit')
