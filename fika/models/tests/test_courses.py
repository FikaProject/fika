from unittest import TestCase

from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject
from pyramid import testing

from fika.models.interfaces import ICourses


class CoursesTests(TestCase):
    
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from fika.models.courses import Courses
        return Courses

    def test_verify_class(self):
        self.failUnless(verifyClass(ICourses, self._cut))

    def test_verify_class(self):
        self.failUnless(verifyObject(ICourses, self._cut()))
