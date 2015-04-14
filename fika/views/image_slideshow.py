from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.view import view_config

from arche.views.base import DefaultView
from arche.views.file import AddFileForm
from arche.utils import generate_slug
from arche import security

from fika.fanstatic import lightbox_js
from fika.fanstatic import lightbox_css
from fika.models.interfaces import IImageSlideshow

 #FIXME: perm check in add
@view_config(context = 'arche.interfaces.IContent', name = 'add', request_param = "content_type=ImageSlideshow",
             permission = security.NO_PERMISSION_REQUIRED, renderer = 'arche:templates/form.pt')
class AddImageSlideshowForm(AddFileForm):
    type_name = u"ImageSlideshow"
    
    def save_success(self, appstruct):
        self.flash_messages.add(self.default_success, type="success")
        factory = self.get_content_factory(self.type_name)
        obj = factory(**appstruct)
        name = generate_slug(self.context, obj.title)
        self.context[name] = obj
        return HTTPFound(location = self.request.resource_url(obj.__parent__))


class ImageSlideshowView(DefaultView):

    @view_config(name = 'inline_in_segment', context = IImageSlideshow, renderer = "fika:templates/image_slideshow.pt",
                  permission=security.PERM_VIEW)
    def image_slideshow_inline(self):
        lightbox_css.need()
        lightbox_js.need()
        super(DefaultView, self).__init__(self.context, self.request)
        response = {}
        return response
        
    @view_config(name = 'view', context = IImageSlideshow, renderer = "fika:templates/image_slideshow.pt",
                  permission=security.PERM_VIEW)
    def image_slideshow(self):
        return HTTPFound(location = self.request.resource_url(self.context.__parent__))
    
    @view_config(context = IImageSlideshow, name = "move_up")
    def move_up(self):
        image_name = self.request.GET.get('image_name')
        new_order = []
        for item in self.context.order:
            if len(new_order) > 0 and image_name == item:
                previous = new_order.pop()
                new_order.append(item)
                new_order.append(previous)
            else:
                new_order.append(item)
        self.context.order = new_order
        return HTTPFound(location = self.request.resource_url(self.context))
    
    @view_config(context = IImageSlideshow, name = "move_down")
    def move_down(self):
        image_name = self.request.GET.get('image_name')
        new_order = []
        temp = None
        for item in self.context.order:
            if image_name == item:
                temp = item
            else:
                new_order.append(item)
                if temp != None:
                    new_order.append(temp)
                    temp = None
        if temp != None:
            new_order.append(temp)
            temp = None
        self.context.order = new_order
        return HTTPFound(location = self.request.resource_url(self.context))
