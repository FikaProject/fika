from pyramid.view import view_config
from pyramid.view import view_defaults
from pyramid.traversal import find_resource
from fika.views.base import BaseView
from fika.models.interfaces import ISiteRoot
from fika import security


@view_defaults(permission = security.VIEW)
class SearchView(BaseView):

    @view_config(context = ISiteRoot, name = "search", renderer = "fika:templates/search.pt")
    def search_view(self):
        query = self.request.GET.get('query', '')
        results = []
        if query:
            docids = self.root.catalog.query("'%s' in searchable_text" % query)[1]
            for docid in docids:
                path = self.root.catalog.document_map.address_for_docid(docid)
                obj = find_resource(self.root, path)
                if self.context_has_permission(obj, security.VIEW):
                    results.append(obj)
        self.response['results'] = results
        return self.response
