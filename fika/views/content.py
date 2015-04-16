from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from arche.views.base import DefaultView
from arche import security
from arche.interfaces import IContent, IImage, IFile
from arche.views.file import mimetype_view_selector

from fika.models.interfaces import IImageSlideshow

class DefaultContentView(DefaultView):

    @view_config(name = 'inline_in_module', context = IContent, renderer = "arche:templates/content/basic.pt",
                  permission=security.PERM_VIEW)
    def default_content_inline(self):
        super(DefaultView, self).__init__(self.context, self.request)
        response = {}
        return response
        
    @view_config(name = '', context = IFile, permission=security.NO_PERMISSION_REQUIRED)
    @view_config(name = 'view', context = IContent, renderer = "arche:templates/content/basic.pt",
                  permission=security.PERM_VIEW)
    def default_content(self):
        return HTTPFound(location = self.request.resource_url(self.context.__parent__))
    
    @view_config(context = IImage, renderer = "arche:templates/content/basic.pt",
                  permission=security.PERM_VIEW)
    def default_image(self):
        if IImageSlideshow.providedBy(self.context.__parent__):
            return HTTPFound(location = self.request.resource_url(self.context.__parent__.__parent__))
        else:
            return HTTPFound(location = self.request.resource_url(self.context.__parent__))


def includeme(config):
    config.add_view(mimetype_view_selector,
                context = 'arche.interfaces.IFile',
                permission = security.PERM_VIEW,
                name = 'inline_in_module')