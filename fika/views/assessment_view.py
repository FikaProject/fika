from pyramid.view import view_config
from pyramid.view import view_defaults
from pyramid.httpexceptions import HTTPFound

from arche import security
from arche.views.base import BaseForm

from fika.models.interfaces import IAssessment

@view_config(name = 'inline', context = IAssessment, renderer = "fika:templates/assessment.pt",
              permission=security.PERM_VIEW)
class AssessmentView(BaseForm):
	type_name = u'Assessment'
	schema_name = 'inline'	
	def __init__(self, context, request):
		return super(BaseForm, self).__init__(context, request)

def includeme(config):
    config.scan('.assessment_view')