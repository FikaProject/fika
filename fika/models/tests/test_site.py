from unittest import TestCase

from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject
from pyramid import testing

from fika.models.interfaces import ISiteRoot


class SiteRootTests(TestCase):
    
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from fika.models.site import SiteRoot
        return SiteRoot

    def test_verify_class(self):
        self.failUnless(verifyClass(ISiteRoot, self._cut))

    def test_verify_class(self):
        self.failUnless(verifyObject(ISiteRoot, self._cut()))
