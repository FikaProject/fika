import colander
import deform

from fika import _

class Assessment(colander.Schema):
    title = colander.SchemaNode(colander.String(),
                                description = _(u"The title of the assessment question. Please include what part of the course or module this question relates to."))
    question = colander.SchemaNode(colander.String(),
    								  description = _(u"The question text."),
                                      widget=deform.widget.RichTextWidget(rows=8, cols=40),
                                      missing = u"")
    email = colander.SchemaNode(colander.String(),
                      description = _(u"Will be displayed in case participants wish to contact the examinator."))

class AssessmentInline(colander.Schema):
	answer = colander.SchemaNode(colander.String(), description = _(u"Type your answer here."),
                                      widget=deform.widget.TextAreaWidget(rows=8, cols=40),
                                      missing = u"")
def includeme(config):
    config.add_content_schema('Assessment', Assessment, 'add')
    config.add_content_schema('Assessment', Assessment, 'edit')
    config.add_content_schema('AssessmentResponse', AssessmentInline, 'add')
    config.add_content_schema('AssessmentResponse', AssessmentInline, 'inline_in_module')

