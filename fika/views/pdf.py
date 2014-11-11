
from arche import security

from fika.views.fika_base_view import FikaBaseView


class PdfView(FikaBaseView):
    def __call__(self):
        return {}


def includeme(config):
    config.add_view(PdfView,
                    name = '__pdf__',
                    context = 'arche.interfaces.IFile',
                    permission = security.PERM_VIEW,
                    renderer = 'fika:templates/pdf.pt')
    config.add_mimetype_view('application/x-pdf', '__pdf__')
    config.add_mimetype_view('application/pdf', '__pdf__')
