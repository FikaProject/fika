import colander
import deform
from betahaus.pyracont.factories import createSchema
from betahaus.pyracont.decorators import content_factory
from zope.interface import implementer

from .base import FikaBaseFolder
from .interfaces import IMediaObject
from .interfaces import ITextMediaObject
from .interfaces import IImageMediaObject
from .interfaces import IImagesMediaObject
from .interfaces import IYoutubeMediaObject
from .interfaces import IVideoMediaObject
from .interfaces import IVimeoMediaObject
from .interfaces import IAudioMediaObject
from .interfaces import IModuleSegment
from .interfaces import ICourseModule
from .interfaces import ICourse
from fika import FikaTSF as _


@implementer(IMediaObject)
class MediaObject(FikaBaseFolder):
    allowed_contexts = (IModuleSegment,)
    schemas = {}
    display_name = _(u"Media object")
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
    display_name = _(u"Text media object")
    icon = u"font"
    
    
    def render(self, request, view):
        return u'<div class="mediaobject">' \
            + self.get_field_value('body', '') \
            + u'</div>'
    
@content_factory('ImageMediaObject')
@implementer(IImageMediaObject)
class ImageMediaObject(MediaObject):
    schemas = {'add': 'ImageMediaObjectSchema',
               'edit': 'ImageMediaObjectSchema',
               'view': 'ImageMediaObjectSchema',
               'delete': 'DeleteSchema'}
    display_name = _(u"Image media object")
    icon = u"picture"
    
    def render(self, request, view):
        return u'<div class="mediaobject"><img class="image-mediaobject" src="' \
            + self.get_field_value('url', '') \
            + u'" /><div>' \
            + self.get_field_value('description', '') \
            + u'</div></div>'
            
@content_factory('ImagesMediaObject')
@implementer(IImagesMediaObject)
class ImagesMediaObject(MediaObject):
    schemas = {'add': 'ImagesMediaObjectSchema',
               'edit': 'ImagesMediaObjectSchema',
               'view': 'ImagesMediaObjectSchema',
               'delete': 'DeleteSchema'}
    display_name = _(u"Images media object")
    icon = u"picture"
    
    def render(self, request, view):
        returnString = u'<div class="mediaobject">'
        for image in self.get_field_value('images', ()):
            returnString += u'<img class="image-mediaobject" src="' \
            + image['url'] \
            + u'" />' \
            + image['image_description']
        returnString += u'<div>' \
            + self.get_field_value('description', '') \
            + u'</div></div>'
        return returnString

@content_factory('YoutubeMediaObject')
@implementer(IYoutubeMediaObject)
class YoutubeMediaObject(MediaObject):
    schemas = {'add': 'YoutubeMediaObjectSchema',
               'edit': 'YoutubeMediaObjectSchema',
               'view': 'YoutubeMediaObjectSchema',
               'delete': 'DeleteSchema'}
    display_name = _(u"Youtube media object")
    icon = u"film"
    
    def render(self, request, view):
        #FIXME: Refactor into template with settings
        return u'<div class="mediaobject"><div class="auto-resizable-iframe"><div><iframe class="youtube" src="//www.youtube.com/embed/' \
            + self.get_field_value('youtube_link', '') \
            + u'" frameborder="0" allowfullscreen></iframe></div></div><div>' \
            + self.get_field_value('description', '') \
            + u'</div></div>'

@content_factory('VimeoMediaObject')
@implementer(IVimeoMediaObject)
class VimeoMediaObject(MediaObject):
    schemas = {'add': 'VimeoMediaObjectSchema',
               'edit': 'VimeoMediaObjectSchema',
               'view': 'VimeoMediaObjectSchema',
               'delete': 'DeleteSchema'}
    display_name = _(u"Vimeo media object")
    icon = u"film"
    
    def render(self, request, view):
        #FIXME: Refactor into template with settings
        return u'<div class="mediaobject"><div class="auto-resizable-iframe"><div><iframe class="youtube" src="//player.vimeo.com/video/' \
            + self.get_field_value('vimeo_link', '') \
            + u'" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe></div></div><div>' \
            + self.get_field_value('description', '') \
            + u'</div></div>'


@content_factory('VideoMediaObject')
@implementer(IVideoMediaObject)
class VideoMediaObject(MediaObject):
    schemas = {'add': 'VideoMediaObjectSchema',
               'edit': 'VideoMediaObjectSchema',
               'view': 'VideoMediaObjectSchema',
               'delete': 'DeleteSchema'}
    display_name = _(u"Video media object")
    icon = u"film"
    
    def render(self, request, view):
        #FIXME: Refactor into template with settings
        return u'<div class="mediaobject"><video controls preload><source src="' \
            + self.get_field_value('video_link', '') \
            + '"  type="video/mp4; codecs=avc1.42E01E,mp4a.40.2"></video>' \
            + self.get_field_value('description', '') \
            + u'</div>'


@content_factory('AudioMediaObject')
@implementer(IAudioMediaObject)
class AudioMediaObject(MediaObject):
    schemas = {'add': 'AudioMediaObjectSchema',
               'edit': 'AudioMediaObjectSchema',
               'view': 'AudioMediaObjectSchema',
               'delete': 'DeleteSchema'}
    display_name = _(u"Audio media object")
    icon = u"headphones"
    
    def render(self, request, view):
        #FIXME: Refactor into template with settings
        return u'<div class="mediaobject"><div><audio controls src="' \
            + self.get_field_value('audio_link', '') \
            +'"></audio></div>' \
            + self.get_field_value('description', '') \
            + u'</div>'


