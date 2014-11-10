import colander
import deform


class AssessmentView(colander.Schema):
	answer = colander.SchemaNode(colander.String(), description = u"Type your answer here.",
                                      validator=colander.Length(max=140),
                                      widget=deform.widget.TextAreaWidget(rows=8, cols=40),
                                      missing = u"")

def includeme(config):
    config.add_content_schema('Assessment', AssessmentView, 'inline')
