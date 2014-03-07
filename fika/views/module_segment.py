import colander
import deform

from js.deform import auto_need
from js.jqueryui import jqueryui

from pyramid.view import view_config
from pyramid.view import view_defaults
from pyramid.httpexceptions import HTTPFound

from betahaus.pyracont.factories import createSchema

from fika import security
from fika.views.base import BaseView
from fika.models.interfaces import IMediaObject
from fika.models.interfaces import IModuleSegment
from fika.models.media_object import YoutubeMediaObject, ImageMediaObject

@view_defaults(permission = security.VIEW)
class ModuleSegment(BaseView):
   
    @view_config(context = IModuleSegment, renderer = "fika:templates/segment.pt")
    def module_segment(self):
        
        #self.response['form'] = self.contextrender(self.request, self)
        return self.response


    @view_config(context = IMediaObject, renderer = "fika:templates/form.pt")
    def media_object(self):
        
        self.response['form'] = self.contextrender(self.request, self)
        return self.response