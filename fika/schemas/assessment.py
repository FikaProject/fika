import colander
import deform


class Assessment(colander.Schema):
    title = colander.SchemaNode(colander.String(),
                                description = u"The title of the assessment question. Please include what part of the course or module this question relates to.")
    description = colander.SchemaNode(colander.String(),
    								  description = u"The question text.",
                                      validator=colander.Length(max=140),
                                      widget=deform.widget.TextAreaWidget(rows=8, cols=40),
                                      missing = u"")

class AssessmentInline(colander.Schema):
	answer = colander.SchemaNode(colander.String(), description = u"Type your answer here.",
                                      validator=colander.Length(max=140),
                                      widget=deform.widget.TextAreaWidget(rows=8, cols=40),
                                      missing = u"")
def includeme(config):
    config.add_content_schema('Assessment', Assessment, 'add')
    config.add_content_schema('Assessment', Assessment, 'edit')
    config.add_content_schema('AssessmentResponse', AssessmentInline, 'inline')

