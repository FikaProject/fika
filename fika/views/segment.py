from pyramid.view import view_config
from pyramid.view import view_defaults
from pyramid.httpexceptions import HTTPFound

from arche import security
from arche.views.base import DefaultView

from fika.models.interfaces import ISegment
from fika.models.image_slideshow import ImageSlideshow
from fika.fanstatic import lightbox_js
from fika.fanstatic import lightbox_css

@view_defaults(permission = security.PERM_VIEW)
class SegmentView(DefaultView):
    
    @view_config(context = ISegment, renderer = "fika:templates/segment.pt", permission=security.PERM_VIEW)
    def segment(self):
        return HTTPFound(location = self.request.resource_url(self.context.__parent__))
    
    @view_config(name = 'inline', context = ISegment, renderer = "fika:templates/segment.pt", permission=security.PERM_VIEW)
    def segment_inline(self):
        response = {}
        response['contents'] = self.context.values()        
        for obj in self.context.values():
            if isinstance(obj, ImageSlideshow):
                lightbox_js.need()
                lightbox_css.need()
                break
        return response
    
def includeme(config):
    config.scan('.segment')
