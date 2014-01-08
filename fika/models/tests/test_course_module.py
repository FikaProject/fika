from unittest import TestCase

from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject
from pyramid import testing

from fika.models.interfaces import ICourseModule


class CourseModuleTests(TestCase):
    
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from fika.models.course_module import CourseModule
        return CourseModule

    def test_verify_class(self):
        self.failUnless(verifyClass(ICourseModule, self._cut))

    def test_verify_class(self):
        self.failUnless(verifyObject(ICourseModule, self._cut()))
