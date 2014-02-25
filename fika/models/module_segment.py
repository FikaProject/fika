import colander
import deform
from betahaus.pyracont.factories import createSchema
from betahaus.pyracont.decorators import content_factory
from zope.interface import implementer

from .base import FikaBaseFolder
from .interfaces import IModuleSegment
from .interfaces import ITextSegment
from .interfaces import IImageSegment
from .interfaces import IYoutubeSegment
from .interfaces import ICourseModule
from .interfaces import ICourse


@implementer(IModuleSegment)
class ModuleSegment(FikaBaseFolder):
    allowed_contexts = (ICourseModule,)
    schemas = {}
    content_type = u""
    icon = u""

    def render(self, request, view):
        schema = createSchema(self.schemas['view'])
        schema = schema.bind(context = self, request = request, view = view)
        form = deform.Form(schema, buttons = (), action="derp")
        appstruct = self.get_field_appstruct(schema)
        return form.render(appstruct = appstruct, readonly = True)
        

@content_factory('TextSegment')
@implementer(ITextSegment)
class TextSegment(ModuleSegment):
    schemas = {'add': 'TextSegmentSchema',
               'edit': 'TextSegmentSchema',
               'view': 'TextSegmentSchema'}
    content_type = u"TextSegment"
    icon = u"font"
    
    
    def render(self, request, view):
        return u'<div class="segment">' + self.get_field_value('body', ()) + u'</div>'
    
@content_factory('ImageSegment')
@implementer(IImageSegment)
class ImageSegment(ModuleSegment):
    schemas = {'add': 'ImageSegmentSchema',
               'edit': 'ImageSegmentSchema',
               'view': 'ImageSegmentSchema'}
    content_type = u"ImageSegment"
    icon = u"picture"
    
    def render(self, request, view):
        return u'<div class="segment"><img class="image-segment" src="' + self.get_field_value('url', ()) + u'" /><div>' + self.get_field_value('description', ()) + u'</div></div>'

@content_factory('YoutubeSegment')
@implementer(IYoutubeSegment)
class YoutubeSegment(ModuleSegment):
    schemas = {'add': 'YoutubeSegmentSchema',
               'edit': 'YoutubeSegmentSchema',
               'view': 'YoutubeSegmentSchema'}
    content_type = u"YoutubeSegment"
    icon = u"film"
    
    def render(self, request, view):
        #FIXME: Refactor into template with settings
        return u'<div class="segment"><iframe width="560" height="315" src="//www.youtube.com/embed/' + self.get_field_value('youtube_link', ()) + u'" frameborder="0" allowfullscreen></iframe><div>' + self.get_field_value('description', ()) + u'</div></div>'
