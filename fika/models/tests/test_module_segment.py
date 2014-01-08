from unittest import TestCase

from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject
from pyramid import testing

from fika.models.interfaces import IModuleSegment


class ModuleSegmentTests(TestCase):
    
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from fika.models.module_segment import ModuleSegment
        return ModuleSegment

    def test_verify_class(self):
        self.failUnless(verifyClass(IModuleSegment, self._cut))

    def test_verify_class(self):
        self.failUnless(verifyObject(IModuleSegment, self._cut()))
