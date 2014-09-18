from pyramid.view import view_config
from pyramid.view import view_defaults

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
