from pyramid.view import view_config

from arche import security
from arche.views.base import BaseForm

from fika.models.interfaces import IAssessment

@view_config(name = 'inline_in_module', context = IAssessment, renderer = "fika:templates/assessment.pt",
              permission=security.PERM_VIEW)
class AssessmentView(BaseForm):
	type_name = u'AssessmentResponse'
	schema_name = 'inline'	
	def __init__(self, context, request):
		return super(BaseForm, self).__init__(context, request)

	def save_success(self, appstruct):
	    self.flash_messages.add(_(u"Response submitted"), type="success")
	    factory = self.get_content_factory(u'AssessmentResponse')
	    # obj = factory(**appstruct)
	    # name = generate_slug(self.context, obj.title)
	    # self.context[name] = obj
	    return HTTPFound(location = self.request.resource_url(self.context))

def includeme(config):
    config.scan('.assessment')