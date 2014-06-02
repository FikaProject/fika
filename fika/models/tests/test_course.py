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

    def test_verify_obj(self):
        self.failUnless(verifyObject(ICourse, self._cut()))


class DeleteCourseTests(TestCase):
    
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _fut(self):
        from fika.models.course import removeUsersFromCourse
        return removeUsersFromCourse
    
    def test_added(self):
        from arche.resources import User
        from arche.resources import Users
        from fika.models.course import Course
        user = User()
        course = Course()
        user.join_course(course)
        self.assertTrue(user.in_course(course))
        root = testing.DummyResource()
        root['users'] = Users()
        root['users'][user.uid] = user
        root['course'] = course
        self._fut(course, None)
        self.assertFalse(user.in_course(course))
