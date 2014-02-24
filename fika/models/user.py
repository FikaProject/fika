from betahaus.pyracont import BaseFolder
from betahaus.pyracont.decorators import content_factory
from zope.interface import implementer
from pyramid.traversal import find_root
from BTrees.OOBTree import OOBTree

from .interfaces import IUser
from .interfaces import IUsers
from .interfaces import ICourse


@content_factory('User')
@implementer(IUser)
class User(BaseFolder):
    allowed_contexts = (IUsers,)
    custom_fields = {'password': 'PasswordField'}
    schemas = {'add': 'UserSchema',
               'edit': 'UserSchema'}

    def __init__(self, data=None, **kwargs):
        super(User, self).__init__(data=None, **kwargs)
        self.__courses__ = OOBTree()

    def default_email(self):
        try:
            return self.get_field_value('validated_emails', ())[0]
        except IndexError:
            return u''

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

