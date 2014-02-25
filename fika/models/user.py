from betahaus.pyracont.decorators import content_factory
from zope.interface import implementer
from pyramid.traversal import find_root
from pyramid.events import subscriber
from BTrees.OOBTree import OOBTree

from .base import FikaBaseFolder
from .interfaces import IUser
from .interfaces import IUsers
from .interfaces import ICourse
from fika import FikaTSF as _
from fika import security
from fika.interfaces import IObjectAddedEvent 


@content_factory('User')
@implementer(IUser)
class User(FikaBaseFolder):
    allowed_contexts = (IUsers,)
    custom_fields = {'password': 'PasswordField'}
    schemas = {'add': 'UserSchema',
               'edit': 'UserSchema',
               'delete': 'DeleteSchema'}

    def __init__(self, data=None, **kwargs):
        super(User, self).__init__(data=None, **kwargs)
        self.__courses__ = OOBTree()

    @property
    def userid(self):
        return self.__name__

    @property
    def title(self):
        return self.get_field_value('name', _(u"(Anonymous)"))

    @property
    def email(self):
        return self.get_field_value('email', '')

    def in_course(self, course):
        assert ICourse.providedBy(course)
        return course.uid in self.__courses__

    def join_course(self, course):
        assert ICourse.providedBy(course)
        self.__courses__[course.uid] = OOBTree()

    def leave_course(self, course):
        assert ICourse.providedBy(course)
        del self.__courses__[course.uid]

    def enrolled_courses(self):
        root = find_root(self)
        courses = root['courses']
        return [root['courses'][x] for x in self.__courses__]


@subscriber([IUser, IObjectAddedEvent])
def setOwner(user, event):
    sec = security.get_security(user)
    sec.add_groups(user.userid, [security.ROLE_OWNER])
