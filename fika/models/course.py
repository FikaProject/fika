from enum import Enum

from arche.interfaces import IBlobs
from arche.interfaces import IObjectWillBeRemovedEvent
from arche.interfaces import IThumbnailedContent
from persistent.list import PersistentList
from pyramid.traversal import find_root
from zope.interface import implementer

from fika import FikaTSF as _
from fika.models.base import FikaBaseFolder
from fika.models.interfaces import ICourse

class CourseStatus(Enum):
    private = 1
    review = 2
    approved =3

@implementer(ICourse, IThumbnailedContent)
class Course(FikaBaseFolder):
    type_title =  _(u"Course")
    type_name = u"Course"
    add_permission = "Add %s" % type_name
    introduction = ""
    status = CourseStatus.private

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

    @property
    def image_data(self): pass
    @image_data.setter
    def image_data(self, value):
        IBlobs(self).create_from_formdata('image', value)


def removeUsersFromCourse(course, event):
    root = find_root(course)
    users = root['users']
    for user in users.values():
        if course.uid in getattr(user, '__courses__', {}):
            del user.__courses__[course.uid]


def includeme(config):
    config.add_content_factory(Course)
    config.add_subscriber(removeUsersFromCourse, [ICourse, IObjectWillBeRemovedEvent])
    config.add_addable_content("Course", "Courses")
