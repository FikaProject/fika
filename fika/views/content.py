from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from arche.views.base import DefaultView
from arche import security
from arche.interfaces import IContent

class DefaultContentView(DefaultView):

    @view_config(name = 'inline', context = IContent, renderer = "arche:templates/content/basic.pt",
                  permission=security.PERM_VIEW)
    def default_content_inline(self):
        print "fika default content inline"
        super(DefaultView, self).__init__(self.context, self.request)
        response = {}
        return response
        
    @view_config(name = 'view', context = IContent, renderer = "arche:templates/content/basic.pt",
                  permission=security.PERM_VIEW)
    def default_content(self):
        print "fika default content"
        return HTTPFound(location = self.request.resource_url(self.context.__parent__.__parent__))


def includeme(config):
    config.scan('.image_slideshow')
