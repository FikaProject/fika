from BTrees.OOBTree import OOBTree
from BTrees.OOBTree import OOSet
from arche.interfaces import IUser
from pyramid.traversal import find_root
from zope.component import adapter
from zope.interface import implementer

from fika import  _
from fika.models.interfaces import ICourse
from fika.models.interfaces import IFikaUser


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
