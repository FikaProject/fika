from pyramid.view import view_config
from pyramid.view import view_defaults
from pyramid.httpexceptions import HTTPFound

from arche import security
from arche import _
from arche.utils import generate_slug
from arche.views.base import BaseForm
from arche.views.base import DefaultView

from fika.models.interfaces import IAssessment

@view_defaults(permission = security.PERM_VIEW)
class AssessmentView(DefaultView):
    
    @view_config(context = IAssessment, permission=security.PERM_VIEW)
    def assessment(self):
        return HTTPFound(location = self.request.resource_url(self.context.__parent__))

@view_config(name = 'inline_in_module', context = IAssessment, renderer = "fika:templates/assessment.pt",
              permission=security.PERM_VIEW)
@view_config(name = 'add', context = IAssessment, renderer = "fika:templates/assessment.pt",
              permission=security.PERM_VIEW)
class AssessmentForm(BaseForm):
    type_name = u'AssessmentResponse'
    schema_name = 'inline_in_module'	
    def __init__(self, context, request):
        return super(AssessmentForm, self).__init__(context, request)

    def save_success(self, appstruct):
        self.flash_messages.add(_(u"Response submitted"), type="success")
        factory = self.get_content_factory(u'AssessmentResponse')
        obj = factory(**appstruct)
        name = generate_slug(self.context, self.profile.title)
        obj.user_uid = self.profile.uid
        self.context[name] = obj
        return HTTPFound(location = self.request.resource_url(self.context))

def includeme(config):
    config.scan('.assessment')