from zope.interface import implementer
#from pyramid.events import subscriber
from pyramid.traversal import find_root
from arche.interfaces import IObjectWillBeRemovedEvent

from .interfaces import ICourse
#from .interfaces import ICourses
from .base import FikaBaseFolder
from fika import FikaTSF as _


@implementer(ICourse)
class Course(FikaBaseFolder):
    #display_name = _(u"Course")
#     schemas = {'add': 'CourseSchema',
#                'edit': 'CourseSchema',
#                'delete': 'DeleteSchema'}
    type_title =  _(u"Course")
    type_name = u"Course"
    addable_to = ("Courses")
    add_permission = "Add %s" % type_name

    def cm_pages(self):
        pages = {0: ''}
        XXX
        for uid in self.get_field_value('course_modules', ()):
            pages[len(pages)] = uid
        return pages


def removeUsersFromCourse(course, event):
    root = find_root(course)
    users = root['users']
    for user in users.values():
        if course.uid in user.__courses__:
            del user.__courses__[course.uid]


def includeme(config):
    config.add_content_factory(Course)
    config.add_subscriber(removeUsersFromCourse, [ICourse, IObjectWillBeRemovedEvent])
