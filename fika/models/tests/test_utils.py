from unittest import TestCase


from pyramid import testing


class FindAllDbObjects(TestCase):
    
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _fut(self):
        from fika.models.utils import find_all_db_objects
        return find_all_db_objects

    def _fixture(self):
        root = testing.DummyResource()
        root['one'] = testing.DummyResource()
        root['one']['1'] = testing.DummyResource()
        root['two'] = testing.DummyResource()
        root['two']['1'] = testing.DummyResource()
        root['two']['2'] = testing.DummyResource()
        root['two']['2']['a'] = testing.DummyResource()
        return root

    def test_find_objects(self):
        res = self._fut(self._fixture())
        self.assertEqual(len(res), 7)
