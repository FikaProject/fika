import colander
import deform
from betahaus.pyracont.decorators import schema_factory

from fika.schemas.common import FileUploadTempStore


@colander.deferred
def file_upload_widget(node, kw):
    request = kw['request']
    tmpstorage = FileUploadTempStore(request)
    return deform.widget.FileUploadWidget(tmpstorage)


@schema_factory()
class AddFileSchema(colander.Schema):
    file = colander.SchemaNode(deform.FileData(),
                               widget = file_upload_widget)


@schema_factory()
class EditFileSchema(colander.Schema):
    pass