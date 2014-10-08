import colander
import deform


class Segment(colander.Schema):
    title = colander.SchemaNode(colander.String(),
                                description = u"The title of the segment.")
    description = colander.SchemaNode(colander.String(),
    								  description = u"A short description of the segment.",
                                      validator=colander.Length(max=140),
                                      widget=deform.widget.TextAreaWidget(rows=8, cols=40),
                                      missing = u"")

def includeme(config):
    config.add_content_schema('Segment', Segment, 'add')
    config.add_content_schema('Segment', Segment, 'edit')
