from unittest import TestCase

from pyramid import testing
from zope.interface import implementer
from betahaus.pyracont import BaseFolder

from fika.models.interfaces import ICatalogable


def _mk_dummy():
    @implementer(ICatalogable)
    class DummyCatalogable(BaseFolder):
        pass
    return DummyCatalogable(title = "Hello world")


class CatalogTests(TestCase):
    
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def _fixture(self):
        from fika.models.site import SiteRoot
        return SiteRoot()

    @property
    def _mud(self):
        from fika.models import catalog
        return catalog

    def test_add_indexable(self):
        root = self._fixture()
        root['one'] = obj = _mk_dummy()
        self._mud.index_object(root.catalog, obj)
        self.assertIn('/one', root.catalog.document_map.address_to_docid)

    def test_add_indexable_correct_interface(self):
        root = self._fixture()
        root['one'] = obj = testing.DummyResource()
        self._mud.index_object(root.catalog, obj)
        self.assertNotIn('/one', root.catalog.document_map.address_to_docid)

    def test_get_title(self):
        pass #FIXME

    def test_get_sortable_title(self):
        pass #FIXME

    def test_get_searchable_text(self):
        pass #FIXME

    def test_get_content_type(self):
        pass #FIXME

    def test_add_subscriber(self):
        root = self._fixture()
        self.config.include('fika.models.catalog')
        root['one'] = _mk_dummy()
        self.assertIn('/one', root.catalog.document_map.address_to_docid)

    def test_update_subscriber(self):
        root = self._fixture()
        cat = root.catalog
        self.config.include('fika.models.catalog')
        root['one'] = _mk_dummy()
        self.assertEqual(cat.query("title == 'Hello world'")[0], 1)
        root['one'].set_field_appstruct({'title': 'Bye world!'})
        self.assertEqual(cat.query("title == 'Hello world'")[0], 0)
        self.assertEqual(cat.query("title == 'Bye world!'")[0], 1)

    def test_remove_subscriber(self):
        root = self._fixture()
        self.config.include('fika.models.catalog')
        root['one'] = _mk_dummy()
        self.assertIn('/one', root.catalog.document_map.address_to_docid)
        del root['one']
        self.assertNotIn('/one', root.catalog.document_map.address_to_docid)

    def test_integration(self):
        self.config.include('fika')
        root = self._fixture()
        root['one'] = _mk_dummy()
        self.assertIn('/one', root.catalog.document_map.address_to_docid)
