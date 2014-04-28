#from betahaus.pyracont.decorators import content_factory
from zope.interface import implementer
from zope.component import adapter
from pyramid.traversal import find_root
from BTrees.OOBTree import OOBTree
from BTrees.OOBTree import OOSet
from arche.interfaces import IUser

from .base import FikaBaseFolder
#from .interfaces import IUser
#from .interfaces import IUsers
from .interfaces import ICourse
from .interfaces import IFikaUser
from fika import  _
#from fika import security
#from fika.interfaces import IObjectAddedEvent 


@adapter(IUser)
@implementer(IFikaUser)
class FikaUser(object):

    def __init__(self, context):
        self.context = context
        if not hasattr(self.context, '__courses__'):
            self.context.__courses__ = OOBTree()
        if not hasattr(self.context, 'completed_course_modules'):
            self.context.completed_course_modules = OOSet()

    @property
    def completed_course_modules(self):
        return self.context.completed_course_modules

    @property
    def courses(self):
        return self.context.__courses__

    def in_course(self, course):
        assert ICourse.providedBy(course)
        return course.uid in self.courses

    def join_course(self, course):
        assert ICourse.providedBy(course)
        self.courses[course.uid] = OOBTree()

    def leave_course(self, course):
        assert ICourse.providedBy(course)
        #FIXME: We propbably want to keep course info though?
        del self.courses[course.uid]

    def enrolled_courses(self):
        root = find_root(self.context)
        courses = root['courses']
        return [courses[x] for x in self.courses]


def includeme(config):
    config.registry.registerAdapter(FikaUser)


#     def __init__(self, data=None, **kwargs):
#         super(User, self).__init__(data=None, **kwargs)
#         self.__courses__ = OOBTree()
#         self.completed_course_modules = OOSet()
# 
#     @property
#     def userid(self):
#         return self.__name__
# 
#     @property
#     def title(self):
#         return self.get_field_value('name', _(u"(Anonymous)"))
# 
#     @property
#     def email(self):
#         return self.get_field_value('email', '')

#     def in_course(self, course):
#         assert ICourse.providedBy(course)
#         return course.uid in self.__courses__
# 
#     def join_course(self, course):
#         assert ICourse.providedBy(course)
#         self.__courses__[course.uid] = OOBTree()
# 
#     def leave_course(self, course):
#         assert ICourse.providedBy(course)
#         #FIXME: We propbably want to keep course info though?
#         del self.__courses__[course.uid]
# 
#     def enrolled_courses(self):
#         root = find_root(self)
#         courses = root['courses']
#         return [root['courses'][x] for x in self.__courses__]


# @subscriber([IUser, IObjectAddedEvent])
# def setOwner(user, event):
#     sec = security.get_security(user)
#     sec.add_groups(user.userid, [security.ROLE_OWNER])
