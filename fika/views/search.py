from pyramid.view import view_config
from pyramid.view import view_defaults
from pyramid.traversal import find_resource
from zope.index.text.parsetree import ParseError
from repoze.catalog.query import Contains

from fika.views.base import BaseView
from fika.models.interfaces import ISiteRoot
from fika import security
from fika import FikaTSF as _


@view_defaults(permission = security.VIEW)
class SearchView(BaseView):

    @view_config(context = ISiteRoot, name = "search", renderer = "fika:templates/search.pt")
    def search_view(self):
        query = self.request.GET.get('query', '')
        self.response['results'] = []
        self.response['query_error'] = None
        if query:
            try:
                qobj = Contains('searchable_text', query)
                docids = self.root.catalog.query(qobj)[1]
            except ParseError:
                self.response['query_error'] = _(u"Invalid query - try again")
                return self.response
            for docid in docids:
                path = self.root.catalog.document_map.address_for_docid(docid)
                obj = find_resource(self.root, path)
                if self.context_has_permission(obj, security.VIEW):
                    self.response['results'].append(obj)
        return self.response
