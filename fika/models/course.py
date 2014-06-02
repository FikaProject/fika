from zope.interface import implementer
#from pyramid.events import subscriber
from pyramid.traversal import find_root
from arche.interfaces import IObjectWillBeRemovedEvent
from persistent.list import PersistentList

from .interfaces import ICourse
#from .interfaces import ICourses
from .base import FikaBaseFolder
from fika import FikaTSF as _


@implementer(ICourse)
class Course(FikaBaseFolder):
    type_title =  _(u"Course")
    type_name = u"Course"
    addable_to = ("Courses",)
    add_permission = "Add %s" % type_name
    introduction = ""

    @property
    def course_modules(self):
        return getattr(self, '_course_modules', ())

    @course_modules.setter
    def course_modules(self, value):
        self._course_modules = PersistentList(value)

    def cm_pages(self):
        pages = {0: ''}
        for uid in self.course_modules:
            pages[len(pages)] = uid
        return pages


def removeUsersFromCourse(course, event):
    root = find_root(course)
    users = root['users']
    for user in users.values():
        if course.uid in getattr(user, '__courses__', {}):
            del user.__courses__[course.uid]


def includeme(config):
    config.add_content_factory(Course)
    config.add_subscriber(removeUsersFromCourse, [ICourse, IObjectWillBeRemovedEvent])
