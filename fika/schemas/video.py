import colander
import deform


class VideoSchema(colander.Schema):
    title = colander.SchemaNode(colander.String(),
                                description=u"The title of the video.",)
    description = colander.SchemaNode(colander.String(),
                                      validator=colander.Length(max=140),
                                      widget=deform.widget.TextAreaWidget(rows=8, cols=40),
                                      missing = u"",
                                      description=u"Write a short description of the video here. Max 140 characters.",)
    choices = (('file', 'MP4 file'), ('youtube', 'Youtube'), ('vimeo', 'Vimeo'))
    video_type = colander.SchemaNode(
        colander.String(),
        validator=colander.OneOf([x[0] for x in choices]),
        widget=deform.widget.RadioChoiceWidget(values=choices),
        title=u'Video type')
    url = colander.SchemaNode(colander.String(),
        title=u'URL',
        description=u"For .mp4 files, the full URL of the video file. For Youtube, the part of the URL between '=' and '&'. For Vimeo, the sequence of numbers in the URL.",)


def includeme(config):
    config.add_content_schema('Video', VideoSchema, 'add')
    config.add_content_schema('Video', VideoSchema, 'edit')
