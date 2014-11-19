from pyramid.view import view_config
from pyramid.view import view_defaults
from pyramid.httpexceptions import HTTPFound

from arche import security
from arche.views.base import DefaultView

from fika.models.interfaces import IAssessment

@view_defaults(permission = security.PERM_VIEW)
class AssesmentView(DefaultView):
    
    @view_config(context = IAssessment, permission=security.PERM_VIEW)
    def assesment(self):
        return HTTPFound(location = self.request.resource_url(self.context.__parent__))
