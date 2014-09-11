from pyramid.httpexceptions import HTTPFound

from arche.views.base import DefaultView
from arche.views.file import AddFileForm
from arche.utils import generate_slug
from arche import security

from fika.fanstatic import lightbox_js
from fika.fanstatic import lightbox_css




class AddImageSlideshowForm(AddFileForm):
    type_name = u"ImageSlideshow"
    
    def save_success(self, appstruct):
        self.flash_messages.add(self.default_success, type="success")
        factory = self.get_content_factory(self.type_name)
        obj = factory(**appstruct)
        name = generate_slug(self.context, obj.title)
        self.context[name] = obj
        return HTTPFound(location = self.request.resource_url(obj))

class ImageSlideshowView(DefaultView):

    def __init__(self, context, request):
        lightbox_css.need()
        lightbox_js.need()
        super(DefaultView, self).__init__(context, request)
        self.response = {}

def includeme(config):
    config.add_view(AddImageSlideshowForm,
                    context = 'arche.interfaces.IContent',
                    name = 'add',
                    request_param = "content_type=ImageSlideshow",
                    permission = security.NO_PERMISSION_REQUIRED, #FIXME: perm check in add
                    renderer = 'arche:templates/form.pt')
    config.add_view(ImageSlideshowView,
                    context = 'fika.models.interfaces.IImageSlideshow',
                    name = 'view',
                    permission = security.PERM_VIEW,
                    renderer = 'fika:templates/image_slideshow.pt') #FIXME: View
