from arche import security
from arche.views.base import BaseView
from pyramid.view import view_config
from pyramid.view import view_defaults

from fika.models.interfaces import IMediaObject
from fika.models.interfaces import IModuleSegment


@view_defaults(permission = security.PERM_VIEW)
class ModuleSegment(BaseView):
   
    @view_config(context = IModuleSegment, renderer = "fika:templates/segment.pt")
    def module_segment(self):
        return {'media_objects': self.context.values()}
