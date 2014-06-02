from pyramid.view import view_config
from pyramid.view import view_defaults
#from pyramid.httpexceptions import HTTPFound
from arche import security
from arche.views.base import BaseView

from fika.models.interfaces import IMediaObject
from fika.models.interfaces import IModuleSegment
from fika.models.media_object import YoutubeMediaObject
from fika.models.media_object import ImageMediaObject
from fika.models.media_object import ImagesMediaObject

@view_defaults(permission = security.PERM_VIEW)
class MediaObject(BaseView):

    @view_config(context = IMediaObject, renderer = "arche:templates/form.pt")
    def media_object(self):
        self.response['form'] = self.context.render(self.request, self)
        return self.response
