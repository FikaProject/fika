from unittest import TestCase

from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject
from pyramid import testing

from fika.models.interfaces import ICourse


class CourseTests(TestCase):
    
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from fika.models.course import Course
        return Course

    def test_verify_class(self):
        self.failUnless(verifyClass(ICourse, self._cut))

    def test_verify_class(self):
        self.failUnless(verifyObject(ICourse, self._cut()))
