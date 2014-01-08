from unittest import TestCase

from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject
from pyramid import testing

from fika.models.interfaces import ICourseModules


class CourseModulesTests(TestCase):
    
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from fika.models.course_modules import CourseModules
        return CourseModules

    def test_verify_class(self):
        self.failUnless(verifyClass(ICourseModules, self._cut))

    def test_verify_class(self):
        self.failUnless(verifyObject(ICourseModules, self._cut()))
