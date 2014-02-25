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



class SetOwnerTests(TestCase):
    
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _fut(self):
        from fika.models.user import setOwner
        return setOwner
    
#     def test_added(self):
#         self.config.include('fika.models.security_mixin')
#         from fika.models.user import User
#         user = User()
#         root = testing.DummyResource()
#         root['user'] = user
#         self._fut(user, None)
#         from fika.models.security_mixin import groupfinder
#         request = testing.DummyRequest()
#         request.context = user
#         self.assertIn('role:Owner', groupfinder('user', request))
    
#     def test_integration(self):
#         self.config.include('fika')
#         from fika.models.user import User
#         user = User()
#         root = testing.DummyResource()
#         root['user'] = user
#         from fika.models.security_mixin import groupfinder
#         request = testing.DummyRequest()
#         request.context = user
#         self.assertIn('role:Owner', groupfinder('user', request))
