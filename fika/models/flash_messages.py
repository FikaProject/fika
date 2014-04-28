import logging

from zope.interface import implementer
from zope.interface.interfaces import ComponentLookupError
from zope.component import adapter
from pyramid.interfaces import IRequest
from pyramid.renderers import render

from fika.models.interfaces import IFlashMessages


log = logging.getLogger(__name__)


@adapter(IRequest)
@implementer(IFlashMessages)
class FlashMessages(object):
    """ See IFlashMessages"""

    def __init__(self, request):
        self.request = request

    def add(self, msg, type='info', dismissable = True, auto_destruct = True):
        css_classes = ['alert']
        css_classes.append('alert-%s' % type)
        if dismissable:
            css_classes.append('alert-dismissable')
        if auto_destruct:
            css_classes.append('fika-auto-destruct')
        css_classes = " ".join(css_classes)
        flash = {'msg':msg, 'dismissable': dismissable, 'css_classes': css_classes}
        self.request.session.flash(flash)

    def get_messages(self):
        for message in self.request.session.pop_flash():
            yield message

    def render(self):
        response = {'get_messages': self.get_messages}
        return render("fika:templates/flash_messages.pt", response, request = self.request)


def get_flash_messages(request):
    try:
        return request.registry.getAdapter(request, IFlashMessages)
    except ComponentLookupError:
        return FlashMessages(request)


#def includeme(config):
#    config.registry.registerAdapter(FlashMessages)
