from uuid import uuid4

from persistent import Persistent
from betahaus.pyracont import utcnow
from betahaus.pyracont.decorators import content_factory
from ZODB.blob import Blob
from zope.interface import implementer

from fika.models.interfaces import IFile
from fika.models.interfaces import IModuleSegment


@content_factory('File')
@implementer(IFile)
class File(Persistent):
    schemas = {'add': 'AddFileSchema', 'edit': 'EditFileSchema', 'delete': 'DeleteSchema'}
    addable_to = ("ModuleSegment",)
    filename = u""
    title = filename
    uid = u""
    icon = u"file"

    def __init__(self,
                 filename = None,
                 fp = None,
                 mimetype = None,
                 **kw):
        self.filename = filename
        self.blobfile = Blob()
        self.mimetype = mimetype
        f = self.blobfile.open('w')
        self.size = upload_stream(fp, f)
        f.close()
        self.uid = uuid4()
        self.created = utcnow()
    
    def render(self, request, view):
        return u'<div class="mediaobject">' \
            + self.filename \
            + u'</div>'

def upload_stream(stream, file):
    size = 0
    while 1:
        data = stream.read(1<<21)
        if not data:
            break
        size += len(data)
        file.write(data)
    return size