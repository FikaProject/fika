from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import effective_principals

from arche import security
from arche import _
from arche.utils import generate_slug
from arche.views.base import BaseForm
from arche.views.base import DefaultView

from fika.models.interfaces import IAssessment

@view_config(name = 'inline_in_module', context = IAssessment, renderer = "fika:templates/assessment.pt",
              permission=security.PERM_VIEW)
@view_config(name = 'add', context = IAssessment, renderer = "fika:templates/assessment.pt",
              permission=security.PERM_VIEW)
class AssessmentForm(BaseForm):
	type_name = u'AssessmentResponse'
	schema_name = 'inline_in_module'	
	def __init__(self, context, request):
		return super(AssessmentForm, self).__init__(context, request)

	def __call__(self):
		if self.request.has_permission('perm:Edit', self.context):
			response = {}
			response['answers'] = self.context.values()   
			return response
		else:
			return super(AssessmentForm, self).__call__()

	def save_success(self, appstruct):
	    self.flash_messages.add(_(u"Response submitted"), type="success")
	    factory = self.get_content_factory(u'AssessmentResponse')
	    obj = factory(**appstruct)
	    name = generate_slug(self.context, self.profile.title)
	    self.context[name] = obj
	    return HTTPFound(location = self.request.resource_url(self.context))

class AssessmentReview(DefaultView):
	@view_config(name = 'inline_in_module', context = IAssessment, renderer = "fika:templates/assessment.pt",
              effective_principals=[security.PERM_EDIT])
	def assessment_review(self):
		import pdb;pdb.set_trace()
		response = {}
		response['answers'] = self.context.values()        
		return response

def includeme(config):
    config.scan('.assessment')