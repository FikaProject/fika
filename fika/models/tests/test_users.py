from unittest import TestCase

from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject
from pyramid import testing

from fika.models.interfaces import IUsers


class UserTests(TestCase):
    
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from fika.models.users import Users
        return Users

    def test_verify_class(self):
        self.failUnless(verifyClass(IUsers, self._cut))

    def test_verify_class(self):
        self.failUnless(verifyObject(IUsers, self._cut()))
