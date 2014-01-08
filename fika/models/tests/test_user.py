from unittest import TestCase

from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject
from pyramid import testing

from fika.models.interfaces import IUser


class UserTests(TestCase):
    
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from fika.models.user import User
        return User

    def test_verify_class(self):
        self.failUnless(verifyClass(IUser, self._cut))

    def test_verify_class(self):
        self.failUnless(verifyObject(IUser, self._cut()))
