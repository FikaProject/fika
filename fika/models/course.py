from arche.api import ContextACLMixin
from arche.api import DCMetadataMixin
from arche.api import LocalRolesMixin
from arche.interfaces import IBlobs
from arche.interfaces import IObjectWillBeRemovedEvent
from arche.interfaces import IThumbnailedContent
from pyramid.traversal import find_root
from zope.interface import implementer

from fika import FikaTSF as _
from fika.models.base import FikaBaseFolder
from fika.models.interfaces import ICourse


@implementer(ICourse, IThumbnailedContent)
class Course(FikaBaseFolder, DCMetadataMixin, LocalRolesMixin, ContextACLMixin):
    type_title =  _(u"Course")
    type_name = u"Course"
    add_permission = "Add %s" % type_name
    introduction = ""

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
