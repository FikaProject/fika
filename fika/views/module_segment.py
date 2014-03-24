from pyramid.view import view_config
from pyramid.view import view_defaults

from fika import security
from fika.views.base import BaseView
from fika.models.interfaces import IMediaObject
from fika.models.interfaces import IModuleSegment


@view_defaults(permission = security.VIEW)
class ModuleSegment(BaseView):
   
    @view_config(context = IModuleSegment, renderer = "fika:templates/segment.pt")
    def module_segment(self):
        self.response['media_objects'] = [x for x in self.context.values() if IMediaObject.providedBy(x)]
        return self.response
