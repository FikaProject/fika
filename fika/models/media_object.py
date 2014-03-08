import colander
import deform
from betahaus.pyracont.factories import createSchema
from betahaus.pyracont.decorators import content_factory
from zope.interface import implementer

from .base import FikaBaseFolder
from .interfaces import IMediaObject
from .interfaces import ITextMediaObject
from .interfaces import IImageMediaObject
from .interfaces import IYoutubeMediaObject
from .interfaces import IModuleSegment
from .interfaces import ICourseModule
from .interfaces import ICourse


@implementer(IMediaObject)
class MediaObject(FikaBaseFolder):
    allowed_contexts = (IModuleSegment,)
    schemas = {}
    content_type = u""
    icon = u""

    def render(self, request, view):
        schema = createSchema(self.schemas['view'])
        schema = schema.bind(context = self, request = request, view = view)
        form = deform.Form(schema, buttons = (), action="derp")
        appstruct = self.get_field_appstruct(schema)
        return form.render(appstruct = appstruct, readonly = True)
        

@content_factory('TextMediaObject')
@implementer(ITextMediaObject)
class TextMediaObject(MediaObject):
    schemas = {'add': 'TextMediaObjectSchema',
               'edit': 'TextMediaObjectSchema',
               'view': 'TextMediaObjectSchema',
               'delete': 'DeleteSchema'}
    content_type = u"TextMediaObject"
    icon = u"font"
    
    
    def render(self, request, view):
        return u'<div class="mediaobject">' + self.get_field_value('body', ()) + u'</div>'
    
@content_factory('ImageMediaObject')
@implementer(IImageMediaObject)
class ImageMediaObject(MediaObject):
    schemas = {'add': 'ImageMediaObjectSchema',
               'edit': 'ImageMediaObjectSchema',
               'view': 'ImageMediaObjectSchema',
               'delete': 'DeleteSchema'}
    content_type = u"ImageMediaObject"
    icon = u"picture"
    
    def render(self, request, view):
        return u'<div class="mediaobject"><img class="image-mediaobject" src="' + self.get_field_value('url', ()) + u'" /><div>' + self.get_field_value('description', ()) + u'</div></div>'

@content_factory('YoutubeMediaObject')
@implementer(IYoutubeMediaObject)
class YoutubeMediaObject(MediaObject):
    schemas = {'add': 'YoutubeMediaObjectSchema',
               'edit': 'YoutubeMediaObjectSchema',
               'view': 'YoutubeMediaObjectSchema',
               'delete': 'DeleteSchema'}
    content_type = u"YoutubeMediaObject"
    icon = u"film"
    
    def render(self, request, view):
        #FIXME: Refactor into template with settings
        return u'<div class="mediaobject"><div class="auto-resizable-iframe"><div><iframe class="youtube" src="//www.youtube.com/embed/' + self.get_field_value('youtube_link', ()) + u'" frameborder="0" allowfullscreen></iframe></div></div><div>' + self.get_field_value('description', ()) + u'</div></div>'
