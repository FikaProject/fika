from betahaus.pyracont.decorators import content_factory
from zope.interface import implementer
from pyramid.events import subscriber
from pyramid.traversal import find_root

from .interfaces import ICourse
from .interfaces import ICourses
from fika.interfaces import IObjectWillBeRemovedEvent
from .base import FikaBaseFolder
from fika import FikaTSF as _


@content_factory('Course')
@implementer(ICourse)
class Course(FikaBaseFolder):
    allowed_contexts = (ICourses,)
    display_name = _(u"Course")
    schemas = {'add': 'CourseSchema',
               'edit': 'CourseSchema',
               'delete': 'DeleteSchema'}

    def cm_pages(self):
        pages = {0: ''}
        for uid in self.get_field_value('course_modules', ()):
            pages[len(pages)] = uid
        return pages

@subscriber([ICourse, IObjectWillBeRemovedEvent])
def removeUsersFromCourse(course, event):
    root = find_root(course)
    users = root['users']
    for user in users.values():
        if course.uid in user.__courses__:
            del user.__courses__[course.uid]