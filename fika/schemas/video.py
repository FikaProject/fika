import colander
from colander import null
from colander import Invalid
import deform
import string

from fika import _

class VideoSchema(colander.Schema):
    title = colander.SchemaNode(colander.String(),
                                description=_(u"The title of the video."),)
    description = colander.SchemaNode(colander.String(),
                                      validator=colander.Length(max=140),
                                      widget=deform.widget.TextAreaWidget(rows=8, cols=40),
                                      missing = u"",
                                      description=_(u"Write a short description of the video here. Max 140 characters."),)
    choices = (('file', _('MP4 file')), ('youtube', _('Youtube')), ('vimeo', _('Vimeo')))
    video_type = colander.SchemaNode(
        colander.String(),
        validator=colander.OneOf([x[0] for x in choices]),
        widget=deform.widget.RadioChoiceWidget(values=choices),
        title=u'Video type')
    url = colander.SchemaNode(colander.String(),
        title=u'URL',
        description=_(u"For .mp4 files, the full URL of the video file. For Youtube, the full URL. For Vimeo, the sequence of numbers in the URL."),)

    def deserialize(self, cstruct):
        # import pdb; pdb.set_trace()
        url_string = cstruct['url']
        if url_string is null:
            return null
        if not isinstance(url_string, basestring):
            raise Invalid(node, _('%r is not a string') % url_string)
        index = string.find(url_string, 'v=')
        if index > 0:
            url_string = url_string[index+2:]
        index = string.find(url_string, 'youtu.be/')
        if index > 0:
            url_string = url_string[index+9:]
        index = string.find(url_string, '&')
        if index > 0:
            url_string = url_string[:index]
        index = string.find(url_string, '#')
        if index > 0:
            url_string = url_string[:index]
        cstruct['url'] = url_string
        return super(VideoSchema, self).deserialize(cstruct)

def includeme(config):
    config.add_content_schema('Video', VideoSchema, 'add')
    config.add_content_schema('Video', VideoSchema, 'edit')
